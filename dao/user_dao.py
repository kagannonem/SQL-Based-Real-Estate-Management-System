import sqlite3
from config import DB_PATH

class UserDAO:
    @staticmethod
    def setup_table():
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT,
            AgentID INTEGER UNIQUE,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            role TEXT CHECK(role IN ('admin','manager','agent')) NOT NULL,
            FOREIGN KEY (AgentID) REFERENCES Agents(AgentID) ON DELETE CASCADE
        );
        """
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute(sql)
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_username(username: str):
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            "SELECT * FROM Users WHERE username = ?", (username,)
        ).fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def create_user(agent_id: int, username: str, hashed_password: str, role: str):
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Users (AgentID, username, hashed_password, role) VALUES (?,?,?,?)",
            (agent_id, username, hashed_password, role)
        )
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id

    @staticmethod
    def get_all():
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        rows = conn.execute("""
            SELECT u.UserID, u.username, u.role, a.AgentName, a.Level
            FROM Users u
            JOIN Agents a ON u.AgentID = a.AgentID
            ORDER BY u.role, a.AgentName
        """).fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def delete_user(user_id: int):
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Users WHERE UserID = ?", (user_id,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0

    @staticmethod
    def get_managed_agent_ids(agent_id: int):
        """Returns list of AgentIDs that this agent directly manages."""
        conn = sqlite3.connect(str(DB_PATH))
        rows = conn.execute(
            "SELECT AgentID FROM Agents WHERE ManagerID = ?", (agent_id,)
        ).fetchall()
        conn.close()
        return [r[0] for r in rows]