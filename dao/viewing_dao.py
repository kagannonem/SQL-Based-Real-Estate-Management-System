import sqlite3
from pathlib import Path

from config import DB_PATH

class ViewingDAO:
    @staticmethod
    def get_all():
        sql = """
            SELECT 
                v.ViewingID, v.ViewingDate, v.Feedback,
                c.ClientName, a.AgentName,
                p.PropertyType, p.District
            FROM Viewings v
            JOIN Clients c ON v.ClientID = c.ClientID
            JOIN Agents a ON v.AgentID = a.AgentID
            JOIN Listings l ON v.ListingID = l.ListingID
            JOIN Properties p ON l.PropertyID = p.PropertyID
            ORDER BY v.ViewingDate DESC;
        """
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def add_viewing(listing_id, client_id, agent_id, viewing_date, feedback=""):
        sql = """
            INSERT INTO Viewings (ListingID, ClientID, AgentID, ViewingDate, Feedback)
            VALUES (?, ?, ?, ?, ?);
        """
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(sql, (listing_id, client_id, agent_id, viewing_date, feedback))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id

    @staticmethod
    def remove_viewing(viewing_id):
        sql = "DELETE FROM Viewings WHERE ViewingID = ?;"
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(sql, (viewing_id,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0
