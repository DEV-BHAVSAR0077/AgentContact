# AgentFlow Deployment Runbook

## 1. Prerequisites
- Python 3.10+
- Node.js 18+ (for frontend)
- Git
- (Optional but recommended) Docker & Docker Compose for Production Sandbox.

## 2. Environment Variables
Copy `.env.example` to `.env` in the `backend/` directory:
```bash
cp .env.example .env
```

Ensure you change `SECRET_KEY` and `DATABASE_URL` appropriately for your deployment.

## 3. Local Development (No Docker)

### Backend
```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

pip install -r requirements.txt
alembic upgrade head
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```
The frontend will be available at `http://localhost:5173`.

## 4. Production Deployment (Docker Compose)
*Note: Docker Compose setup is pending for V2.*

In the meantime, run the backend behind a reverse proxy (like Nginx) and serve the frontend statically using `npm run build`.

## 5. Troubleshooting
- **Database Locked Errors**: If using SQLite, ensure only one process is migrating the DB at a time.
- **WebSocket Drops**: Check if your reverse proxy supports WebSocket upgrading.
- **Sandbox Execution Failures**: If Docker is not available, the `SandboxAdapter` will fall back to local process simulation. This will log `Simulated sandbox execution`.
