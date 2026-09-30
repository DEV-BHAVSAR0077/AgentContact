#!/usr/bin/env pwsh

Write-Host "Starting AgentFlow..." -ForegroundColor Green

# Start backend
Start-Process -NoNewWindow -FilePath "powershell.exe" -ArgumentList "-Command `"cd backend; .\venv\Scripts\activate; uvicorn app.main:app --reload --port 8000`""

# Start frontend
Start-Process -NoNewWindow -FilePath "powershell.exe" -ArgumentList "-Command `"cd frontend; npm run dev`""

Write-Host "AgentFlow is running!" -ForegroundColor Green
Write-Host "Frontend: http://localhost:5173" -ForegroundColor Blue
Write-Host "Backend API: http://localhost:8000/docs" -ForegroundColor Blue
