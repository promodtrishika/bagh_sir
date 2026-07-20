**Live demo:** 
https://bagh-sir-tools.streamlit.app
# BAGH_SIR — Bagh's Shape-Integrated Reckoner

**Volume, bulk density and macroporosity of asteroids and comets from 3D shape models, plus a physical-plausibility audit of the SiMDA catalogue.**

Promod Bagh · Independent researcher · Raghunathpur, India

---

## What this is

BAGH_SIR is a small, transparent Python tool that:

1. Computes the **true volume** of an asteroid or comet from its published 3D shape model (`.obj` mesh), using the standard signed-tetrahedron sum, cross-checked by an independent projection (prism) method. The two methods agree to machine precision on every body tested.
2. Derives **bulk density** (given a mass) and **macroporosity** (given a rock type or grain density).
3. Reports **shape uncertainty** — how far a sphere or ellipsoid assumption would have been off for that particular body.
4. Applies a **physical-plausibility audit** to the SiMDA catalogue: any published bulk density exceeding the grain density of the body's own rock type is physically impossible (porosity can only lower density), and is flagged with a predicted correction.

**This is established computational geometry — a validated, transparent implementation, not new mathematics.** The value is in the careful application, the two-way verification, the open code, and the audit.

## Validation

Where shape models carry true physical scale (spacecraft targets), the tool reproduces the published bulk density with no size fitting:

| Body | Mission | BAGH_SIR ρ | Published ρ |
|---|---|---|---|
| 67P (comet) | Rosetta / ESA | 0.535 | 0.536 |
| Bennu | OSIRIS-REx / NASA | 1.190 | 1.190 |
| Ryugu | Hayabusa2 / JAXA | 1.195 | 1.19 |
| Itokawa | Hayabusa / JAXA | 1.865 | 1.9 |

For scale-free catalogue models (DAMIT), the pipeline recovers the SiMDA density exactly — this is a **consistency check, not a validation**, since the scaling step reuses the catalogue diameter (agreement is guaranteed by construction). This distinction is stated deliberately; see `docs/BAGH_SIR_Validation_Record_REVISED.docx`.

## The audit and its falsifiable predictions

Several carbonaceous (C/P class) asteroids in SiMDA carry published bulk densities of 4.5–6.1 g/cm³ — above the ~2.2–2.9 g/cm³ grain density of carbonaceous meteorites, which is physically impossible. Since their diameters are well measured, the masses are implicated. Predicted corrections (stated in advance so future measurements can test them):

| Asteroid | Published ρ | Prediction |
|---|---|---|
| (206) Hersilia (C) | 6.08 | mass ≈ 0.6–0.8×10¹⁸ kg → ρ 1.3–1.7 |
| (410) Chloris (C) | 4.96 | mass ≈ 1.2–1.6×10¹⁸ kg → ρ 1.3–1.7 |
| (34) Circe (C) | 4.63 | mass ≈ 1.0–1.3×10¹⁸ kg → ρ 1.3–1.7 |
| (102) Miriam (P) | 4.46 | mass ≈ 0.4–0.5×10¹⁸ kg → ρ 1.0–1.5 |
| (110) Lydia (M) | 4.88 | diameter 86–95 km → ρ 2.7–3.7 |

The full flagged list (19 tier-1 bodies and further tiers) is in `data/density_audit_candidates.csv`.

**Relation to prior work (stated plainly):** the bulk-vs-grain-density framework is standard (Britt et al. 2002); Carry (2012) attached quality ranks flagging unrealistic densities, from which SiMDA's "X" rank descends; and Hanuš et al. (2013) already concluded (34) Circe's mass is overestimated by ~2× — the same factor this audit derives independently. A newer ephemeris mass for (102) Miriam (Fienga et al. 2020) moves its density partway toward the predicted range. This work **independently reproduces and systematizes** those concerns for the current SiMDA catalogue, with open code and explicit predicted ranges.

## Repository contents

```
code/
  small_body_volume.py     command-line tool: self-test, single shape, batch mode
  small_body_volume_5.py   variant with porosity output
  bagh_sir.py              Streamlit web interface
data/
  candidate_masses.csv         name, mass_kg, diam_km per body (batch input)
  density_audit_candidates.csv full SiMDA plausibility audit, tiered
  results.csv                  batch output, ranked by shape uncertainty
docs/
  BAGH_SIR_Complete_Explanation.docx            full technical account, honest assessment
  BAGH_SIR_Validation_Record_REVISED.docx       validation vs consistency check, clearly separated
  BAGH_SIR_Math_Worked_Examples_Illustrated.docx  every formula with worked examples and diagrams
```

## Quick start

```bash
pip install numpy scipy

# self-test on exact shapes (cube, sphere)
python3 code/small_body_volume.py

# one asteroid: shape + mass + known diameter
python3 code/small_body_volume.py bennu.obj 7.329e10

# batch: every .obj in a folder, with masses/diameters from CSV
python3 code/small_body_volume.py --batch models/ data/candidate_masses.csv
```

Shape models (free): [DAMIT](https://astro.troja.mff.cuni.cz/projects/damit/), [NASA PDS](https://sbn.psi.edu/pds/shape-models/), JAXA DARTS, 3d-asteroids.space.

**Note:** the SiMDA catalogue itself is not redistributed here. Download it from the SiMDA project (Kretlow 2020, Zenodo / https://astro.kretlow.de/simda) under its own terms.

## References

- Britt, D. T., Yeomans, D., Housen, K., Consolmagno, G. (2002). Asteroid density, porosity, and structure. *Asteroids III*, 485–500.
- Carry, B. (2012). Density of asteroids. *Planetary and Space Science*, 73(1), 98–118.
- Hanuš, J. et al. (2013). Sizes of main-belt asteroids by combining shape models and Keck adaptive-optics observations. *Icarus*.
- Fienga, A., Avdellidou, C., Hanuš, J. (2020). Asteroid masses obtained with INPOP planetary ephemerides. *MNRAS*, 492(1), 589.
- Kretlow, M. (2020). Size, Mass and Density of Asteroids (SiMDA). *EPSC Abstracts* 14, EPSC2020-690.
- Mission densities: Lauretta et al. 2019 (Bennu); Watanabe et al. 2019 (Ryugu); Fujiwara et al. 2006 (Itokawa); Pätzold et al. 2016 (67P).

## License

MIT — see `LICENSE`.

## Citing this work

See `CITATION.cff`, or cite the Zenodo DOI of this release (added after the first Zenodo upload).
