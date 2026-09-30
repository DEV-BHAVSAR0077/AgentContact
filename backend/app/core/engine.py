import asyncio
import traceback
from datetime import datetime, timezone
from typing import List, Dict, Any
from sqlalchemy import select
from app.models.db import Execution

class GraphEngine:
    """
    V1 Native Graph Engine.
    Executes a graph topologically and handles failures cleanly.
    """
    def __init__(self, execution_id: str, nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]], broadcast_callback: Any) -> None:
        self.execution_id = execution_id
        self.nodes = {n["id"]: n for n in nodes}
        self.edges = edges
        self.broadcast = broadcast_callback
        
    async def run(self) -> None:
        from app.core.database import engine, async_sessionmaker
        SessionLocal = async_sessionmaker(engine, expire_on_commit=False)
        
        try:
            # Simulate topological execution
            for node_id, node in self.nodes.items():
                await self._broadcast_log(node_id, "RUNNING", f"Executing node {node.get('type', 'Unknown')}")
                
                # Mock execution work
                await asyncio.sleep(1)
                
                if node.get('type') == 'fail_mock':
                    raise ValueError(f"Simulated failure at node {node_id}")
                
                await self._broadcast_log(node_id, "COMPLETED", f"Completed node {node.get('type', 'Unknown')}")

            # Success
            async with SessionLocal() as db:
                result = await db.execute(select(Execution).where(Execution.id == self.execution_id))
                execution = result.scalars().first()
                if execution:
                    execution.status = "COMPLETED"
                    execution.completed_at = datetime.now(timezone.utc)
                    await db.commit()
            
            await self.broadcast(self.execution_id, {"type": "status", "status": "COMPLETED"})
            
        except Exception as e:
            error_msg = str(e)
            trace = traceback.format_exc()
            
            # Failure
            async with SessionLocal() as db:
                result = await db.execute(select(Execution).where(Execution.id == self.execution_id))
                execution = result.scalars().first()
                if execution:
                    execution.status = "FAILED"
                    execution.error = f"{error_msg}\n{trace}"
                    execution.completed_at = datetime.now(timezone.utc)
                    await db.commit()
                    
            await self.broadcast(self.execution_id, {
                "type": "status", 
                "status": "FAILED", 
                "error": error_msg
            })

    async def _broadcast_log(self, node_id: str, status: str, message: str) -> None:
        await self.broadcast(self.execution_id, {
            "type": "log",
            "nodeId": node_id,
            "status": status,
            "message": message
        })
