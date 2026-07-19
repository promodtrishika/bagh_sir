"""
BAGH_SIR - Streamlit web app
============================
Bagh's Shape-Integrated Reckoner - volume, density & porosity from a 3D shape model
by Promod Bagh, Independent researcher, Raghunathpur, India

Deploy free on Streamlit Community Cloud:
  main file path:  streamlit_app.py
"""
import io
import numpy as np
import pandas as pd
import streamlit as st

# ================================================================
# CORE MATH  (identical to code/bagh_sir.py / small_body_volume.py)
# ================================================================

def collapse_shape(V, F):
    v0, v1, v2 = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    footprint = 0.5 * ((v1[:, 0] - v0[:, 0]) * (v2[:, 1] - v0[:, 1])
                       - (v2[:, 0] - v0[:, 0]) * (v1[:, 1] - v0[:, 1]))
    mean_depth = (v0[:, 2] + v1[:, 2] + v2[:, 2]) / 3.0
    return footprint, mean_depth

def rebuild_by_inverse_collapse(footprint, mean_depth):
    return abs((footprint * mean_depth).sum())

def genesis_volume(V, F):
    v0, v1, v2 = V[F[:, 0]], V[F[:, 1]], V[F[:, 2]]
    return abs(np.einsum('ij,ij->i', v0, np.cross(v1, v2)).sum()) / 6.0

def volume_sphere(V):
    r = ((V.max(0) - V.min(0)) / 2.0).mean()
    return 4.0 / 3.0 * np.pi * r ** 3

def volume_ellipsoid(V):
    C = V - V.mean(0)
    _, _, axes = np.linalg.svd(C, full_matrices=False)
    a, b, c = ((C @ axes.T).max(0) - (C @ axes.T).min(0)) / 2.0
    return 4.0 / 3.0 * np.pi * a * b * c

def volume_hull(V):
    try:
        from scipy.spatial import ConvexHull
        return ConvexHull(V).volume
    except Exception:
        return np.nan

def equiv_diameter(vol):
    return (6.0 * vol / np.pi) ** (1.0 / 3.0)

def scale_to_diameter(V, F, target_diam):
    cur = equiv_diameter(genesis_volume(V, F))
    return V.astype(float) * (target_diam / cur), cur

GRAIN = {
    "C": 2.73, "B": 2.73, "G": 2.70, "F": 2.70, "P": 2.60, "D": 2.60, "T": 2.70,
    "S": 3.73, "Q": 3.73, "K": 3.50, "L": 3.50, "A": 3.70,
    "V": 3.26, "E": 3.00, "R": 3.40,
    "M": 4.90, "X": 4.90,
}

def porosity(bulk, taxon=None, grain=None):
    if grain is None and taxon:
        grain = GRAIN.get(taxon[0].upper())
    if not grain:
        return None, None, ""
    p = 1.0 - bulk / grain
    if p < 0:      label = "bulk > grain: check size, mass, or rock type"
    elif p < 0.10: label = "solid / coherent rock"
    elif p < 0.30: label = "fractured / microporous"
    else:          label = "rubble pile (high macroporosity)"
    return p, grain, label

def read_obj_text(text):
    verts, faces = [], []
    for line in text.splitlines():
        if line.startswith("v "):
            verts.append([float(x) for x in line.split()[1:4]])
        elif line.startswith("f "):
            idx = [int(t.split("/")[0]) - 1 for t in line.split()[1:]]
            for k in range(1, len(idx) - 1):
                faces.append([idx[0], idx[k], idx[k + 1]])
    return np.array(verts, float), np.array(faces, int)

# ================================================================
# UI
# ================================================================

st.set_page_config(page_title="BAGH_SIR", page_icon="🪨", layout="centered")

st.title("BAGH_SIR")
st.caption("Bagh's Shape-Integrated Reckoner — volume, density & porosity from a 3D shape model")

st.markdown(
    "Upload an asteroid or comet **.obj** shape model. BAGH_SIR computes its true volume "
    "from the real shape (not a sphere guess), then its bulk density and porosity. "
    "The volume code has been validated against spacecraft-visited bodies — **Bennu** "
    "(NASA OSIRIS-REx), **Ryugu** (JAXA Hayabusa2), **Itokawa** (JAXA Hayabusa) and "
    "**comet 67P** (ESA Rosetta) — reproducing each published density from the "
    "absolutely-scaled mission shape models."
)

with st.expander("Example values to try"):
    st.markdown(
        "- **Bennu**: mass `7.329e10` kg — mission model is in km, no diameter needed\n"
        "- **Lydia** (DAMIT model): mass `6.32e18` kg, diameter `86` km, rock type `M`\n"
        "- Free shape models: [DAMIT](https://astro.troja.mff.cuni.cz/projects/damit/), "
        "[NASA PDS](https://sbn.psi.edu/pds/shape-models/), JAXA DARTS, 3d-asteroids.space"
    )

up = st.file_uploader("Shape model (.obj)", type=["obj"])

c1, c2 = st.columns(2)
with c1:
    mass_s = st.text_input("Mass in kg (optional — needed for density)", placeholder="e.g. 7.33e10")
with c2:
    diam_s = st.text_input("Known diameter in km (optional — scales the shape)", placeholder="e.g. 0.49")

st.markdown("**Porosity** (optional) — choose a rock type *or* enter a grain density:")
c3, c4 = st.columns(2)
with c3:
    taxon = st.selectbox("Rock type", ["(none)"] + sorted(GRAIN.keys()))
with c4:
    grain_s = st.text_input("or grain density (g/cm³)", placeholder="e.g. 2.4")

if st.button("Analyze", type="primary", use_container_width=True):
    if up is None:
        st.warning("Please upload an .obj shape model first.")
        st.stop()
    try:
        V, F = read_obj_text(up.getvalue().decode("utf-8", errors="ignore"))
        if len(V) < 4 or len(F) < 4:
            st.error("Could not read a valid mesh from this file.")
            st.stop()
    except Exception as e:
        st.error(f"Could not parse the .obj file: {e}")
        st.stop()

    mass = float(mass_s) if mass_s.strip() else None
    tdiam = float(diam_s) if diam_s.strip() else None
    grain = float(grain_s) if grain_s.strip() else None
    tx = None if taxon == "(none)" else taxon

    orig_d = None
    if tdiam:
        V, orig_d = scale_to_diameter(V, F, tdiam)

    fp, md = collapse_shape(V, F)
    Vc = rebuild_by_inverse_collapse(fp, md)
    Vg = genesis_volume(V, F)
    match = abs(Vc - Vg) < max(Vg * 1e-6, 1e-12)

    Vsph, Vell, Vhul = volume_sphere(V), volume_ellipsoid(V), volume_hull(V)
    vols = np.array([v for v in (Vsph, Vell, Vhul, Vg) if not np.isnan(v)])
    spread = (vols.max() - vols.min()) / Vg * 100.0
    dEq = equiv_diameter(Vg)

    if match:
        st.success(f"Done — {len(V):,} vertices, {len(F):,} faces. Both volume methods agreed.")
    else:
        st.error(f"Warning — the two volume methods DISAGREE ({Vc:.6g} vs {Vg:.6g}). "
                 "The mesh may not be closed or consistently oriented; results below are unreliable.")

    unit = "km" if tdiam else "model units"
    m1, m2, m3 = st.columns(3)
    m1.metric("True volume", f"{Vg:.4g} ({unit})³")
    m2.metric("Equivalent diameter", f"{dEq:.4g} {unit}")
    m3.metric("Shape uncertainty", f"{spread:.1f}%",
              help="How far a round-shape assumption (sphere/ellipsoid) would be from the real mesh volume.")

    if orig_d:
        st.caption(f"Model scaled from equivalent diameter {orig_d:.4g} (model units) to the known {tdiam:g} km.")

    if mass:
        if tdiam:
            rho = mass / (Vg * 1e12)   # km^3 + kg -> g/cm^3
            st.metric("Bulk density", f"{rho:.3f} g/cm³")
            p, g, label = porosity(rho, tx, grain)
            if p is not None:
                st.metric("Macroporosity", f"{p*100:.0f}%", help=f"grain density used: {g:.2f} g/cm³")
                st.info(f"Interpretation: **{label}**")
        else:
            st.warning("Density needs a physical scale: the mesh must be in km already "
                       "(spacecraft models) or you must give a known diameter. "
                       "If this mission model is already in km, the density is:")
            rho = mass / (Vg * 1e12)
            st.metric("Bulk density (assuming mesh is in km)", f"{rho:.3f} g/cm³")
            p, g, label = porosity(rho, tx, grain)
            if p is not None:
                st.metric("Macroporosity", f"{p*100:.0f}%", help=f"grain density used: {g:.2f} g/cm³")
                st.info(f"Interpretation: **{label}**")

    st.subheader("Why shape matters")
    st.caption("The same body, measured four ways. The real mesh is the truth; "
               "the others show how far a simpler assumption would be off.")
    df = pd.DataFrame({
        "Method": ["Sphere guess", "Ellipsoid guess", "Convex hull", "Real mesh (BAGH_SIR)"],
        f"Volume ({unit})³": [f"{Vsph:.4g}", f"{Vell:.4g}",
                              f"{Vhul:.4g}" if not np.isnan(Vhul) else "n/a", f"{Vg:.4g}"],
        "vs real": [f"{(Vsph/Vg-1)*100:+.0f}%", f"{(Vell/Vg-1)*100:+.0f}%",
                    f"{(Vhul/Vg-1)*100:+.0f}%" if not np.isnan(Vhul) else "n/a", "—"],
    })
    st.table(df)

st.divider()
st.caption(
    "BAGH_SIR uses standard computational geometry — two independent volume methods "
    "(signed-tetrahedron sum + projection) that agree to machine precision. "
    "A validated, transparent tool, not new physics. · Built by Promod Bagh, "
    "Independent researcher, Raghunathpur, India. · "
    "Code & data: [github.com/promodtrishika/bagh_sir](https://github.com/promodtrishika/bagh_sir) · "
    "Archived: [doi.org/10.5281/zenodo.21433683](https://doi.org/10.5281/zenodo.21433683)"
)
