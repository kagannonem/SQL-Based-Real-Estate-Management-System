"""
Run once: python3 migrate_targets.py
Creates the AgentTargets table in real_estate.db
"""
import sqlite3
from config import DB_PATH

conn = sqlite3.connect(str(DB_PATH))
conn.executescript("""
CREATE TABLE IF NOT EXISTS AgentTargets (
    TargetID        INTEGER PRIMARY KEY AUTOINCREMENT,
    AgentID         INTEGER NOT NULL,
    ManagerID       INTEGER NOT NULL,
    Year            INTEGER NOT NULL,
    Quarter         INTEGER NOT NULL CHECK(Quarter IN (1,2,3,4)),
    TargetViewings  INTEGER DEFAULT 0,
    TargetListings  INTEGER DEFAULT 0,
    TargetRevenue   REAL    DEFAULT 0,
    UNIQUE(AgentID, Year, Quarter),
    FOREIGN KEY (AgentID)   REFERENCES Agents(AgentID) ON DELETE CASCADE,
    FOREIGN KEY (ManagerID) REFERENCES Agents(AgentID) ON DELETE CASCADE
);
""")
conn.commit()
conn.close()
print("✅ AgentTargets table created (or already exists).")