# PowerShell helper to run the app via the package entrypoint
# Usage: ./run.ps1

$python = "C:/Users/vishe/.virtualenvs/vishe-Tprebq5r/Scripts/python.exe"
& $python -m uvicorn insuremate.main:app --host 127.0.0.1 --port 8000 --reload
