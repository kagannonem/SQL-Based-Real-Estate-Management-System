"""
target_routes.py — Agent performance targets & actuals

Mount in app.py:
    from target_routes import router as target_router
    app.include_router(target_router)
"""

import sqlite3
from datetime import date
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from auth import get_current_user, require_role
from config import DB_PATH

router = APIRouter(prefix="/api/targets", tags=["targets"])


# ── helpers ────────────────────────────────────────────────────────────────────

def get_conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def current_quarter() -> tuple[int, int]:
    today = date.today()
    return today.year, (today.month - 1) // 3 + 1

def _actuals(conn, agent_id: int, year: int, quarter: int) -> dict:
    """Compute actual viewings, closed listings, and revenue for a quarter."""
    # quarter date bounds  e.g. Q2 → 04-01 .. 06-30
    m_start = (quarter - 1) * 3 + 1
    m_end   = quarter * 3
    d_start = f"{year}-{m_start:02d}-01"
    # last day of m_end (simple approach)
    import calendar
    last_day = calendar.monthrange(year, m_end)[1]
    d_end    = f"{year}-{m_end:02d}-{last_day:02d}"

    viewings = conn.execute(
        "SELECT COUNT(*) FROM Viewings WHERE AgentID=? AND ViewingDate BETWEEN ? AND ?",
        (agent_id, d_start, d_end)
    ).fetchone()[0]

    listings_closed = conn.execute(
        "SELECT COUNT(*) FROM Listings WHERE AgentID=? AND Status='Closed' AND EndDate BETWEEN ? AND ?",
        (agent_id, d_start, d_end)
    ).fetchone()[0]

    revenue = conn.execute(
        "SELECT COALESCE(SUM(Amount),0) FROM Transactions WHERE AgentID=? AND TransactionDate BETWEEN ? AND ?",
        (agent_id, d_start, d_end)
    ).fetchone()[0]

    return {"viewings": viewings, "listings_closed": listings_closed, "revenue": revenue}


# ── schemas ────────────────────────────────────────────────────────────────────

class TargetUpsert(BaseModel):
    agent_id: int
    year: Optional[int] = None     # defaults to current year
    quarter: Optional[int] = None  # defaults to current quarter
    target_viewings: int = 0
    target_listings: int = 0
    target_revenue: float = 0


# ── endpoints ─────────────────────────────────────────────────────────────────

@router.post("")
def upsert_target(body: TargetUpsert, user=Depends(require_role("admin", "manager"))):
    """Manager sets or updates targets for one of their direct agents."""
    year, quarter = body.year or current_quarter()[0], body.quarter or current_quarter()[1]

    conn = get_conn()
    # Verify the target agent actually reports to this manager (managers only)
    if user["role"] == "manager":
        row = conn.execute(
            "SELECT AgentID FROM Agents WHERE AgentID=? AND ManagerID=?",
            (body.agent_id, user["agent_id"])
        ).fetchone()
        if not row:
            conn.close()
            raise HTTPException(status_code=403, detail="You can only set targets for your direct reports")

    manager_id = user["agent_id"] if user["role"] == "manager" else (
        conn.execute("SELECT ManagerID FROM Agents WHERE AgentID=?", (body.agent_id,)).fetchone()["ManagerID"] or user["agent_id"]
    )

    conn.execute("""
        INSERT INTO AgentTargets (AgentID, ManagerID, Year, Quarter, TargetViewings, TargetListings, TargetRevenue)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(AgentID, Year, Quarter) DO UPDATE SET
            TargetViewings = excluded.TargetViewings,
            TargetListings = excluded.TargetListings,
            TargetRevenue  = excluded.TargetRevenue,
            ManagerID      = excluded.ManagerID
    """, (body.agent_id, manager_id, year, quarter,
          body.target_viewings, body.target_listings, body.target_revenue))
    conn.commit()
    conn.close()
    return {"status": "success"}


@router.get("/my")
def get_my_targets(user=Depends(get_current_user)):
    """Agent sees their own current-quarter targets + actuals."""
    agent_id = user["agent_id"]
    if not agent_id:
        raise HTTPException(status_code=400, detail="No agent profile linked to this user")

    year, quarter = current_quarter()
    conn = get_conn()

    target_row = conn.execute(
        "SELECT * FROM AgentTargets WHERE AgentID=? AND Year=? AND Quarter=?",
        (agent_id, year, quarter)
    ).fetchone()

    actuals = _actuals(conn, agent_id, year, quarter)
    conn.close()

    target = dict(target_row) if target_row else {
        "TargetViewings": 0, "TargetListings": 0, "TargetRevenue": 0
    }

    return {
        "status": "success",
        "data": {
            "year": year,
            "quarter": quarter,
            "targets": {
                "viewings":  target["TargetViewings"],
                "listings":  target["TargetListings"],
                "revenue":   target["TargetRevenue"],
            },
            "actuals": actuals,
        }
    }


@router.get("/team")
def get_team_targets(user=Depends(require_role("admin", "manager"))):
    """Manager sees all direct reports with targets + actuals for current quarter."""
    year, quarter = current_quarter()
    manager_id = user["agent_id"]

    conn = get_conn()

    # Get direct reports
    if user["role"] == "manager":
        agents = conn.execute(
            "SELECT AgentID, AgentName, Level FROM Agents WHERE ManagerID=?",
            (manager_id,)
        ).fetchall()
    else:
        # admin sees everyone
        agents = conn.execute(
            "SELECT AgentID, AgentName, Level FROM Agents ORDER BY AgentName"
        ).fetchall()

    result = []
    for a in agents:
        aid = a["AgentID"]
        target_row = conn.execute(
            "SELECT * FROM AgentTargets WHERE AgentID=? AND Year=? AND Quarter=?",
            (aid, year, quarter)
        ).fetchone()
        actuals = _actuals(conn, aid, year, quarter)
        target = dict(target_row) if target_row else {
            "TargetViewings": 0, "TargetListings": 0, "TargetRevenue": 0
        }
        result.append({
            "agent_id":   aid,
            "agent_name": a["AgentName"],
            "level":      a["Level"],
            "year":       year,
            "quarter":    quarter,
            "targets": {
                "viewings": target["TargetViewings"],
                "listings": target["TargetListings"],
                "revenue":  target["TargetRevenue"],
            },
            "actuals": actuals,
        })

    conn.close()
    return {"status": "success", "data": result, "year": year, "quarter": quarter}


@router.get("/team/{agent_id}")
def get_agent_targets_history(agent_id: int, user=Depends(require_role("admin", "manager"))):
    """Get all quarterly targets for a specific agent (for history/editing)."""
    conn = get_conn()

    if user["role"] == "manager":
        row = conn.execute(
            "SELECT AgentID FROM Agents WHERE AgentID=? AND ManagerID=?",
            (agent_id, user["agent_id"])
        ).fetchone()
        if not row:
            conn.close()
            raise HTTPException(status_code=403, detail="Not your direct report")

    targets = conn.execute(
        "SELECT * FROM AgentTargets WHERE AgentID=? ORDER BY Year DESC, Quarter DESC",
        (agent_id,)
    ).fetchall()
    conn.close()
    return {"status": "success", "data": [dict(t) for t in targets]}
