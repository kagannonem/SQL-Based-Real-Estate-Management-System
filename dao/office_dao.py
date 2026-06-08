import sqlite3
from pathlib import Path

from config import DB_PATH

class OfficeDAO:
    @staticmethod
    def get_all():
        sql = "SELECT * FROM Offices;"
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]

    @staticmethod
    def add_office(name, city, district, phone, email):
        sql = """
            INSERT INTO Offices (OfficeName, City, District, PhoneNumber, Email)
            VALUES (?, ?, ?, ?, ?);
        """
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(sql, (name, city, district, phone, email))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id

    @staticmethod
    def remove_office(office_id):
        sql = "DELETE FROM Offices WHERE OfficeID = ?;"
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(sql, (office_id,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0
