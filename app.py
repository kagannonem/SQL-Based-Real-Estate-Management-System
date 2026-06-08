from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dao.agent_dao import AgentDAO
from dao.property_dao import PropertyDAO
from dao.client_dao import ClientDAO
from dao.listing_dao import ListingDAO
from dao.viewing_dao import ViewingDAO
from dao.transaction_dao import TransactionDAO
from dao.office_dao import OfficeDAO
from dao.user_dao import UserDAO
import sqlite3
from auth import get_current_user, require_role
from auth_routes import router as auth_router
from target_routes import router as target_router 
from pathlib import Path
from config import DB_PATH

app = FastAPI(title="Real Estate Management System API")

app.include_router(auth_router)
app.include_router(target_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AgentCreateInput(BaseModel):
    office_id: int
    name: str
    email: str
    manager_id: Optional[int] = None
    level: str

class PropertyCreateInput(BaseModel):
    property_type: str
    city: str
    district: str
    area: float
    asking_price: float
    status: str = "Available"

class StatusUpdateInput(BaseModel):
    status: str

class ClientCreateInput(BaseModel):
    name: str
    phone: str
    mail: str
    client_type: str
    reg_date: str

class ListingCreateInput(BaseModel):
    property_id: int
    agent_id: int
    owner_id: int
    start_date: str
    listing_price: float

class ViewingCreateInput(BaseModel):
    listing_id: int
    client_id: int
    agent_id: int
    viewing_date: str
    feedback: Optional[str] = ""

class TransactionCreateInput(BaseModel):
    listing_id: int
    buyer_id: int
    agent_id: int
    amount: float
    transaction_date: str

class OfficeCreateInput(BaseModel):
    name: str
    city: str
    district: str
    phone: str
    email: str


@app.get("/")
def serve_frontend():
    return FileResponse("index.html")


# ── AGENTS ────────────────────────────────────────────────────────────────────

@app.get("/api/agents/hierarchy")
def get_agents_hierarchy(user=Depends(get_current_user)):
    return {"status": "success", "data": AgentDAO.get_management_hierarchy()}

@app.get("/api/agents/simple")
def get_agents_simple(user=Depends(get_current_user)):
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT AgentID, AgentName FROM Agents ORDER BY AgentName").fetchall()
    conn.close()
    return {"status": "success", "data": [dict(r) for r in rows]}

@app.get("/api/agents")
def get_all_agents(user=Depends(get_current_user)):
    return {"status": "success", "data": AgentDAO.get_management_hierarchy()}

@app.post("/api/agents")
def create_agent(agent: AgentCreateInput, user=Depends(require_role("admin", "manager"))):
    # Managers can only add agents that report to themselves
    if user["role"] == "manager":
        agent.manager_id = user["agent_id"]
    new_id = AgentDAO.add_agent(agent.office_id, agent.name, agent.email, agent.manager_id, agent.level)
    return {"status": "success", "agent_id": new_id}

@app.delete("/api/agents/{agent_id}")
def delete_agent(agent_id: int, user=Depends(require_role("admin", "manager"))):
    if user["role"] == "manager":
        managed = UserDAO.get_managed_agent_ids(user["agent_id"])
        if agent_id not in managed:
            raise HTTPException(status_code=403, detail="You can only remove agents you directly manage")
    success = AgentDAO.remove_agent(agent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"status": "success"}


# ── PROPERTIES ────────────────────────────────────────────────────────────────

@app.get("/api/properties/stats")
def get_property_stats(user=Depends(get_current_user)):
    return {"status": "success", "data": PropertyDAO.get_avg_price_by_district()}

@app.get("/api/properties/simple")
def get_properties_simple(user=Depends(get_current_user)):
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT PropertyID, PropertyType, District FROM Properties ORDER BY PropertyID").fetchall()
    conn.close()
    return {"status": "success", "data": [dict(r) for r in rows]}

@app.get("/api/properties/{property_id}")
def get_property(property_id: int, user=Depends(get_current_user)):
    row = PropertyDAO.get_by_id(property_id)
    if not row:
        raise HTTPException(status_code=404, detail="Property not found")
    return {"status": "success", "data": row}

@app.get("/api/properties")
def get_properties(user=Depends(get_current_user)):
    return {"status": "success", "data": PropertyDAO.get_all()}

@app.post("/api/properties")
def create_property(p: PropertyCreateInput, user=Depends(get_current_user)):
    new_id = PropertyDAO.add_property(p.property_type, p.city, p.district, p.area, p.asking_price, p.status)
    return {"status": "success", "property_id": new_id}

@app.patch("/api/properties/{property_id}/status")
def update_property_status(property_id: int, body: StatusUpdateInput, user=Depends(require_role("admin", "manager"))):
    success = PropertyDAO.update_status(property_id, body.status)
    if not success:
        raise HTTPException(status_code=404, detail="Property not found")
    return {"status": "success"}

@app.delete("/api/properties/{property_id}")
def delete_property(property_id: int, user=Depends(require_role("admin"))):
    success = PropertyDAO.remove_property(property_id)
    if not success:
        raise HTTPException(status_code=404, detail="Property not found")
    return {"status": "success"}


# ── CLIENTS ───────────────────────────────────────────────────────────────────

@app.get("/api/clients/simple")
def get_clients_simple(user=Depends(get_current_user)):
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT ClientID, ClientName FROM Clients ORDER BY ClientName").fetchall()
    conn.close()
    return {"status": "success", "data": [dict(r) for r in rows]}

@app.get("/api/clients")
def get_clients(user=Depends(get_current_user)):
    return {"status": "success", "data": ClientDAO.get_all()}

@app.post("/api/clients")
def create_client(c: ClientCreateInput, user=Depends(get_current_user)):
    new_id = ClientDAO.add_client(c.name, c.phone, c.mail, c.client_type, c.reg_date)
    return {"status": "success", "client_id": new_id}

@app.delete("/api/clients/{client_id}")
def delete_client(client_id: int, user=Depends(require_role("admin"))):
    success = ClientDAO.remove_client(client_id)
    if not success:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"status": "success"}


# ── LISTINGS ──────────────────────────────────────────────────────────────────

@app.get("/api/listings/simple")
def get_listings_simple(user=Depends(get_current_user)):
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    rows = conn.execute("SELECT ListingID, Status FROM Listings ORDER BY ListingID").fetchall()
    conn.close()
    return {"status": "success", "data": [dict(r) for r in rows]}

@app.get("/api/listings/active")
def get_active_listings(user=Depends(get_current_user)):
    return {"status": "success", "data": ListingDAO.get_active()}

@app.get("/api/listings/viewings-count")
def get_listing_viewing_counts(user=Depends(get_current_user)):
    return {"status": "success", "data": ListingDAO.get_viewing_counts()}

@app.get("/api/listings")
def get_listings(user=Depends(get_current_user)):
    return {"status": "success", "data": ListingDAO.get_all()}

@app.post("/api/listings")
def create_listing(l: ListingCreateInput, user=Depends(get_current_user)):
    new_id = ListingDAO.add_listing(l.property_id, l.agent_id, l.owner_id, l.start_date, l.listing_price)
    return {"status": "success", "listing_id": new_id}

@app.delete("/api/listings/{listing_id}")
def delete_listing(listing_id: int, user=Depends(require_role("admin", "manager"))):
    success = ListingDAO.remove_listing(listing_id)
    if not success:
        raise HTTPException(status_code=404, detail="Listing not found")
    return {"status": "success"}


# ── VIEWINGS ──────────────────────────────────────────────────────────────────

@app.get("/api/viewings")
def get_viewings(user=Depends(get_current_user)):
    return {"status": "success", "data": ViewingDAO.get_all()}

@app.post("/api/viewings")
def create_viewing(v: ViewingCreateInput, user=Depends(get_current_user)):
    new_id = ViewingDAO.add_viewing(v.listing_id, v.client_id, v.agent_id, v.viewing_date, v.feedback)
    return {"status": "success", "viewing_id": new_id}

@app.delete("/api/viewings/{viewing_id}")
def delete_viewing(viewing_id: int, user=Depends(require_role("admin", "manager"))):
    success = ViewingDAO.remove_viewing(viewing_id)
    if not success:
        raise HTTPException(status_code=404, detail="Viewing not found")
    return {"status": "success"}


# ── TRANSACTIONS ──────────────────────────────────────────────────────────────

@app.get("/api/transactions/revenue")
def get_revenue_by_agent(user=Depends(get_current_user)):
    return {"status": "success", "data": TransactionDAO.get_revenue_by_agent()}

@app.get("/api/transactions")
def get_transactions(user=Depends(get_current_user)):
    return {"status": "success", "data": TransactionDAO.get_all()}

@app.post("/api/transactions")
def create_transaction(t: TransactionCreateInput, user=Depends(get_current_user)):
    new_id = TransactionDAO.add_transaction(t.listing_id, t.buyer_id, t.agent_id, t.amount, t.transaction_date)
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute("UPDATE Listings SET Status='Closed', EndDate=? WHERE ListingID=?", (t.transaction_date, t.listing_id))
    conn.execute("UPDATE Properties SET Status='Sold' WHERE PropertyID=(SELECT PropertyID FROM Listings WHERE ListingID=?)", (t.listing_id,))
    conn.commit()
    conn.close()
    return {"status": "success", "transaction_id": new_id}


# ── OFFICES ───────────────────────────────────────────────────────────────────

@app.get("/api/offices")
def get_offices(user=Depends(get_current_user)):
    return {"status": "success", "data": OfficeDAO.get_all()}

@app.post("/api/offices")
def create_office(o: OfficeCreateInput, user=Depends(require_role("admin"))):
    new_id = OfficeDAO.add_office(o.name, o.city, o.district, o.phone, o.email)
    return {"status": "success", "office_id": new_id}

@app.delete("/api/offices/{office_id}")
def delete_office(office_id: int, user=Depends(require_role("admin"))):
    success = OfficeDAO.remove_office(office_id)
    if not success:
        raise HTTPException(status_code=404, detail="Office not found")
    return {"status": "success"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
