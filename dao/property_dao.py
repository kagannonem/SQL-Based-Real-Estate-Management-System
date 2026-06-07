import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.parent.resolve()
DB_PATH = PROJECT_DIR / "real_estate.db"

class PropertyDAO:
    @staticmethod
    def get_all():
        sql = "SELECT * FROM Properties;"
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        results = [dict(row) for row in rows]
        conn.close()
        return results

    @staticmethod
    def get_by_id(property_id):
        sql = "SELECT * FROM Properties WHERE PropertyID = ?;"
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql, (property_id,))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def add_property(property_type, city, district, area, asking_price, status="Available"):
        sql = """
            INSERT INTO Properties (PropertyType, City, District, Area, AskingPrice, Status)
            VALUES (?, ?, ?, ?, ?, ?);
        """
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(sql, (property_type, city, district, area, asking_price, status))
        new_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return new_id

    @staticmethod
    def update_status(property_id, status):
        sql = "UPDATE Properties SET Status = ? WHERE PropertyID = ?;"
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(sql, (status, property_id))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0

    @staticmethod
    def remove_property(property_id):
        sql = "DELETE FROM Properties WHERE PropertyID = ?;"
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute(sql, (property_id,))
        affected = cursor.rowcount
        conn.commit()
        conn.close()
        return affected > 0

    @staticmethod
    def get_avg_price_by_district():
        sql = """
            SELECT District, COUNT(*) as total, AVG(AskingPrice) as avg_price
            FROM Properties
            GROUP BY District
            ORDER BY avg_price DESC;
        """
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return [dict(row) for row in rows]
