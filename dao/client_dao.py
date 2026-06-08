import sqlite3
from pathlib import Path

from config import DB_PATH

class ClientDAO:
    @staticmethod
    def get_all():
        sql = "SELECT * FROM Clients ORDER BY RegDate DESC;"
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(client_id):
        sql = "SELECT * FROM Clients WHERE ClientID = ?;"
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql, (client_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def add_client(name, phone, mail, client_type, reg_date):
        sql = """
            INSERT INTO Clients (ClientName, ClientPhone, ClientMail, ClientType, RegDate)
            VALUES (?, ?, ?, ?, ?);
        """
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(sql, (name, phone, mail, client_type, reg_date))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id

    @staticmethod
    def remove_client(client_id):
        sql = "DELETE FROM Clients WHERE ClientID = ?;"
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(sql, (client_id,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0

    @staticmethod
    def get_buyers_and_sellers():
        sql = """
            SELECT ClientName, ClientType, ClientPhone, ClientMail
            FROM Clients
            WHERE ClientType IN ('Buyer', 'Both')
            ORDER BY ClientType;
        """
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
