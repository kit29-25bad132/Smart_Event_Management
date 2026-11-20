# Windows PowerShell setup

```powershell
cd backend
py -3.14 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn app.main:app --reload --port 8000
```

In a second terminal:

```powershell
cd frontend
Copy-Item .env.example .env.local
npm install
npm run dev
```

Open `http://localhost:3000`. API checks: `http://localhost:8000/api/health` and `/api/ready`.
