import sqlite3
from pathlib import Path

from config import DB_PATH

class ListingDAO:
    @staticmethod
    def get_all():
        sql = """
            SELECT 
                l.ListingID, l.Status, l.ListingPrice, l.StartDate, l.EndDate,
                p.PropertyType, p.City, p.District, p.Area,
                a.AgentName, c.ClientName AS OwnerName
            FROM Listings l
            JOIN Properties p ON l.PropertyID = p.PropertyID
            JOIN Agents a ON l.AgentID = a.AgentID
            JOIN Clients c ON l.OwnerID = c.ClientID
            ORDER BY l.StartDate DESC;
        """
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_active():
        sql = """
            SELECT 
                l.ListingID, l.ListingPrice, l.StartDate,
                p.PropertyType, p.City, p.District, p.Area,
                a.AgentName
            FROM Listings l
            JOIN Properties p ON l.PropertyID = p.PropertyID
            JOIN Agents a ON l.AgentID = a.AgentID
            WHERE l.Status = 'Active'
            ORDER BY l.ListingPrice ASC;
        """
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def add_listing(property_id, agent_id, owner_id, start_date, listing_price):
        sql = """
            INSERT INTO Listings (PropertyID, AgentID, OwnerID, StartDate, ListingPrice, Status)
            VALUES (?, ?, ?, ?, ?, 'Active');
        """
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(sql, (property_id, agent_id, owner_id, start_date, listing_price))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id

    @staticmethod
    def remove_listing(listing_id):
        sql = "DELETE FROM Listings WHERE ListingID = ?;"
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(sql, (listing_id,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0

    @staticmethod
    def get_viewing_counts():
        sql = """
            SELECT l.ListingID, p.PropertyType, p.District, COUNT(v.ViewingID) as viewing_count
            FROM Listings l
            JOIN Properties p ON l.PropertyID = p.PropertyID
            LEFT JOIN Viewings v ON l.ListingID = v.ListingID
            GROUP BY l.ListingID
            ORDER BY viewing_count DESC;
        """
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
