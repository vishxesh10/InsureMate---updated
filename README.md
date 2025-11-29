# InsureMate — project structure

This repo contains the InsureMate insurance premium prediction app.

I created a recommended, production-friendly package layout under
`insuremate/` so you can migrate from the single-file layout gradually.

What I added (safe scaffolding that does not remove your current code):

- `insuremate/`
  - `main.py` — package entrypoint (imports the existing `app` in root `app.py`)
  - `api/` — place to split route routers (stubs created)
  - `db/` — placeholder to centralize DB helpers (imports your existing `database.py`)
  - `services/` — place to put ML/prediction logic and helpers
- `tests/` — top-level directory for tests

How to run (no immediate code moves required):

- Current working app is still the `app.py` at project root. You can run it as before:

```powershell
# run existing entry
C:/Users/vishe/.virtualenvs/vishe-Tprebq5r/Scripts/python.exe -m uvicorn app:app --host 127.0.0.1 --port 8000
```

- To use the package entrypoint (pointing to the same app) run:

```powershell
C:/Users/vishe/.virtualenvs/vishe-Tprebq5r/Scripts/python.exe -m uvicorn insuremate.main:app --host 127.0.0.1 --port 8000
```

Migration suggestions (next steps):

1. Move route code from `app.py` into `insuremate/api/` routers (e.g. `predict.py`) and include them in `insuremate/main.py`.
2. Move `database.py` into `insuremate/db/` and update imports to the new package path.
3. Move ML pre/post-processing into `insuremate/services/` and call from routers.
4. Add tests under `tests/` for endpoints and services.

If you want, I can perform the migration (move code into packages, update imports, and run tests).
