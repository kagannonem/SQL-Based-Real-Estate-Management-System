import sqlite3
from pathlib import Path

from config import DB_PATH

class TransactionDAO:
    @staticmethod
    def get_all():
        sql = """
            SELECT 
                t.TransactionID, t.Amount, t.TransactionDate,
                buyer.ClientName AS BuyerName,
                a.AgentName,
                p.PropertyType, p.District
            FROM Transactions t
            JOIN Clients buyer ON t.BuyerID = buyer.ClientID
            JOIN Agents a ON t.AgentID = a.AgentID
            JOIN Listings l ON t.ListingID = l.ListingID
            JOIN Properties p ON l.PropertyID = p.PropertyID
            ORDER BY t.TransactionDate DESC;
        """
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def add_transaction(listing_id, buyer_id, agent_id, amount, transaction_date):
        sql = """
            INSERT INTO Transactions (ListingID, BuyerID, AgentID, Amount, TransactionDate)
            VALUES (?, ?, ?, ?, ?);
        """
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(sql, (listing_id, buyer_id, agent_id, amount, transaction_date))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id

    @staticmethod
    def get_revenue_by_agent():
        sql = """
            SELECT 
                a.AgentName,
                COUNT(t.TransactionID) as total_deals,
                SUM(t.Amount) as total_revenue
            FROM Transactions t
            JOIN Agents a ON t.AgentID = a.AgentID
            GROUP BY a.AgentID
            ORDER BY total_revenue DESC;
        """
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
