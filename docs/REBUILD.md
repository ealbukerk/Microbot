# Rebuilding V7

Use Python 3.10+ and install the analysis/render dependencies in a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cd designs/v7
```

On Windows activate `.venv\Scripts\activate` instead. FreeCAD needs its own built-in Python/Part modules; `.FCMacro` files run inside FreeCAD, not ordinary Python. FFmpeg must be on PATH for video rendering. Node.js is used only for mesh/transform checks. A compatible Unicode TrueType font improves render labels; render scripts fall back when platform fonts are absent.

## Build order

1. `python design_board.py` — package placement.
2. `python plan_assembly.py` — six-second geometric trajectory; requires NumPy.
3. Open `BuildSphere.FCMacro` in FreeCAD and execute it. It saves bot/14-bot CAD, STEP, BOM, mesh, screenshots and CAD report, then closes its generated documents/application. Save unrelated FreeCAD work before running.
4. Execute `AuditInertia.FCMacro` in FreeCAD. It exports inertias and samples the custom gear mesh, then closes FreeCAD.
5. `python analyze.py` — mass/inertia, nominal inverse-dynamics and reserve screening.
6. `python audit_topology.py` — ideal pin/rail connectivity versus flat-dock contact.
7. `python check_electrical.py` — block-level and scalar electrical checks.
8. `python cost_and_layout.py` — current unquoted cost inputs and board illustration.
9. `python publish_v7.py` — full web specification/cost tables, V7 report and component dimensions.
10. Optional: `python render_animation.py` and `python render_cutaway.py` — regenerate media; animation rendering needs FFmpeg.
11. `node check_models.mjs` — mesh indices, finite geometry and rigid-transform checks. Existing browser evidence is accepted only when it matches the current mesh hash; this does not automate or prove a hardware test.

`write_report.py` is retained as the earlier V6 report generator. Use `publish_v7.py` for V7 reporting. Browser verification screenshots/JSON record the imported local session; rerun and document browser verification after changes. A changed mesh invalidates its stored browser hash.

The component selection and cost models contain assumptions. A successful rebuild does not complete the missing mechanical, electronic or wireless engineering. See `PROJECT_STATE.md`.
