import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent.resolve()
DB_PATH = PROJECT_DIR / "real_estate.db"

class AgentDAO:
    @staticmethod
    def get_management_hierarchy():
        sql_query = """
            SELECT 
                subordinate.AgentName AS employee,
                subordinate.Level AS emp_level,
                manager.AgentName AS reports_to,
                manager.Level AS mgr_level
            FROM Agents subordinate
            LEFT JOIN Agents manager ON subordinate.ManagerID = manager.AgentID;
        """
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql_query)
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
        conn.close()
        return results

    @staticmethod
    def add_agent(office_id, name, email, manager_id, level):
        """Inserts a new agent record into the database."""
        sql_query = """
            INSERT INTO Agents (OfficeID, AgentName, Email, ManagerID, Level)
            VALUES (?, ?, ?, ?, ?);
        """
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(sql_query, (office_id, name, email, manager_id, level))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id

    @staticmethod
    def remove_agent(agent_id):
        """Deletes an agent. Note: Foreign keys will handle ON DELETE SET NULL for subordinates!"""
        sql_query = "DELETE FROM Agents WHERE AgentID = ?;"
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(sql_query, (agent_id,))
        rows_affected = cursor.rowcount
        conn.commit()
        conn.close()
        return rows_affected > 0