# AgentFlow

AgentFlow is a visual AI/ML multi-agent orchestration platform where users can create AI agents/models as visual nodes, connect those nodes using edges, and execute the connected graph as a real backend workflow.

## Features (MVP)
* **Visual Graph Builder**: React Flow based node editor
* **Agent Nodes & Model Nodes**: Distinct visual nodes for Agents and Models (APIs & Scikit-Learn placeholders)
* **Execution Engine**: Real-time websocket logs output simulating backend execution topology.
* **Dashboard**: Statistics on Agents, Models, and Workflows.
* **Modern UI**: Tailored with Tailwind CSS and Lucide React.
* **FastAPI Backend**: Real robust API with SQLite for persistence out of the box, ready for PostgreSQL migration.

## Tech Stack
* **Frontend**: React, Vite, Tailwind CSS, React Flow (@xyflow/react), Zustand
* **Backend**: FastAPI, SQLAlchemy, SQLite (for MVP local setup), Uvicorn

## How to Run

1. Open PowerShell and run the initialization script to start both Frontend and Backend:
```powershell
.\start.ps1
```

2. Wait for the servers to start.
3. Open `http://localhost:5173` to view the UI.
4. Open `http://localhost:8000/docs` to view the OpenAPI documentation.

## Architecture

- `backend/app/main.py`: Entrypoint for FastAPI
- `backend/app/models/db.py`: SQLAlchemy schemas
- `backend/app/schemas/domain.py`: Pydantic Schemas
- `backend/app/api/endpoints/`: Routing logic
- `frontend/src/pages/`: Core application pages
- `frontend/src/components/nodes/`: Custom React Flow nodes

## Future Work / Production Enhancements
* Replace SQLite with PostgreSQL in `backend/app/core/config.py`
* Setup Redis and Celery for distributed background task execution.
* Integrate actual Model Sandboxes for PyTorch/Pickle models.
