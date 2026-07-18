# UPLOAD GUIDE — GitHub + Zenodo, step by step

Follow these steps in order. Total time: about 30–45 minutes. Everything is free.
The goal: your code and predictions get a permanent, dated DOI that proves
you stated the Hersilia / Chloris / Circe / Miriam / Lydia predictions in advance.

---

## PART A — GitHub (the living repository)

1. Go to https://github.com and sign in (or create a free account).

2. Click the "+" (top right) → "New repository".
   - Repository name: `bagh_sir`
   - Description: "Volume, density & porosity of asteroids from 3D shape models + SiMDA plausibility audit"
   - Public
   - Do NOT tick "Add a README" (you already have one)
   - Click "Create repository".

3. Upload the files. Easiest way (no command line needed):
   - On the new empty repository page, click "uploading an existing file".
   - Drag the ENTIRE CONTENTS of this folder (README.md, LICENSE, CITATION.cff,
     .zenodo.json, requirements.txt, and the code/, data/, docs/ folders)
     into the upload box. GitHub keeps the folder structure.
   - Commit message: "Initial release v1.0.0"
   - Click "Commit changes".

4. Fix one placeholder: open CITATION.cff on GitHub, click the pencil (edit),
   and replace YOUR_USERNAME in the repository-code line with your actual
   GitHub username. Commit.

5. Create a Release (Zenodo needs this):
   - On the repository page, right sidebar → "Releases" → "Create a new release".
   - Tag: `v1.0.0`
   - Release title: `BAGH_SIR v1.0.0 — first public release`
   - Description: one or two sentences, e.g.
     "First public release. Volume tool validated against Bennu, Ryugu,
      Itokawa and 67P; SiMDA plausibility audit with falsifiable predictions
      for Hersilia, Chloris, Circe, Miriam and Lydia."
   - Click "Publish release".

---

## PART B — Zenodo (the permanent DOI)

Option 1 — automatic (recommended):

1. Go to https://zenodo.org and click "Sign up" → "Sign up with GitHub".
   This links the two accounts.
2. In Zenodo: click your account (top right) → "GitHub".
3. Find `bagh_sir` in the repository list and flip its switch ON.
4. Go back to GitHub and publish a new release (e.g. tag `v1.0.1`, title
   "Zenodo archive release" — a release made AFTER the switch is on triggers
   the archive). Zenodo automatically archives it and mints a DOI within minutes.
5. In Zenodo → "GitHub" page, click the DOI badge next to your repository
   to see your DOI (it looks like 10.5281/zenodo.XXXXXXX).

Option 2 — manual (if the GitHub link gives trouble):

1. On https://zenodo.org click "New upload".
2. Upload the zip of this folder (bagh_sir_release.zip).
3. Fill the form — the .zenodo.json in this folder contains the exact text
   to copy: title, description, keywords, license (MIT), upload type (Software).
4. Under "Related works" you may add the SiMDA dataset: search Zenodo for
   "SiMDA Kretlow" and use its DOI with relation "Is derived from".
5. Click "Publish". Your DOI appears immediately.

---

## PART C — after you have the DOI (5 minutes)

1. Edit README.md on GitHub: in the "Citing this work" section, add the DOI,
   e.g. "Archived at Zenodo: https://doi.org/10.5281/zenodo.XXXXXXX".
2. Edit CITATION.cff: add a line
   `doi: "10.5281/zenodo.XXXXXXX"`
3. Zenodo also gives you a badge (Markdown snippet) — paste it at the top
   of README.md if you like.

That's it. From this moment your predictions are timestamped, citable,
and permanently archived. Anyone — including a future you writing the
Minor Planet Bulletin note — can cite:

   Bagh, P. (2026). BAGH_SIR: volume, density and macroporosity of small
   bodies from 3D shape models, with a physical-plausibility audit of the
   SiMDA catalogue (v1.0.0). Zenodo. https://doi.org/10.5281/zenodo.XXXXXXX

---

## Notes

- The SiMDA.csv catalogue file is deliberately NOT included in this release —
  it is Kretlow's dataset and people should download it from the SiMDA
  project directly. The README says so and links it.
- Everything under docs/ is companion material; the journal submission
  (Minor Planet Bulletin) will be a separate, freshly written note that
  cites this DOI.
- If you later improve the code, just publish a new GitHub release —
  Zenodo automatically archives each release under a new version DOI,
  while one "concept DOI" always points to the latest version.
