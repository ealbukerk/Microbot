# Contributing

1. Open an issue describing the problem, proposed requirement or failed check.
2. Fork the repository or, if you have write access, create a branch.
3. Make the change and submit a pull request with its purpose, affected requirements, calculations/checks and remaining limitations.
4. Keep nominal calculations, simulated behavior, supplier ratings and measured hardware results distinct. Include test setup, units and evidence for new performance claims.

## Source and outputs

Current sources and outputs live together in `designs/v7` so the static viewer resolves its assets. Update the relevant Python/FreeCAD source before rebuilding generated files. Avoid editing CAD meshes or report numbers by hand. The cost caps are goals, not supplier prices.

FreeCAD files are binary: coordinate substantial CAD edits before working concurrently. The `.FCMacro` sources are text and are the preferred place to review parametric changes. Include corresponding CAD exports and reports when geometry changes. Do not commit FreeCAD autosave/backups, environment files, credentials, runtime caches or full conversation logs.

See `docs/REBUILD.md` for build order and checks. Pull requests should explain what was tested and what was not. Do not claim complete hardware validation without that evidence; clearly record the open work.

The owner must select a project license and invite named direct-write collaborators. Fork-and-PR review remains the default collaboration path.
