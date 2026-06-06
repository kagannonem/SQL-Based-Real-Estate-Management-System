from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dao.agent_dao import AgentDAO

app = FastAPI(title="Real Estate Management System API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# A data structure validator for creating a new agent
class AgentCreateInput(BaseModel):
    office_id: int
    name: str
    email: str
    manager_id: Optional[int] = None
    level: str

@app.get("/api/agents/hierarchy")
def get_agents_hierarchy():
    return {"status": "success", "data": AgentDAO.get_management_hierarchy()}

@app.post("/api/agents")
def create_agent(agent: AgentCreateInput):
    """Endpoint for the admin to add a new agent."""
    try:
        new_id = AgentDAO.add_agent(
            agent.office_id, agent.name, agent.email, agent.manager_id, agent.level
        )
        return {"status": "success", "message": "Agent created successfully", "agent_id": new_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/api/agents/{agent_id}")
def delete_agent(agent_id: int):
    """Endpoint for the admin to remove an agent by ID."""
    success = AgentDAO.remove_agent(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"status": "success", "message": f"Agent {agent_id} successfully removed"}

if __name__ == "__main__":
    import uvicorn
    # This must be "app:app", NOT "app.py:app"
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)