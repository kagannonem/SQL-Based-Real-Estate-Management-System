import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.resolve()
DB_PATH = PROJECT_DIR / "real_estate.db"
SQL_FILE_PATH = PROJECT_DIR / "test_queries.sql"

def execute_test_query():
    if not SQL_FILE_PATH.exists():
        print(f"❌ Error: Please create '{SQL_FILE_PATH.name}' first.")
        return

    # Read the SQL instructions you wrote in your .sql file
    with open(SQL_FILE_PATH, "r", encoding="utf-8") as f:
        sql_query = f.read().strip()

    if not sql_query:
        print("⚠️ Your 'test_queries.sql' file is empty!")
        return

    try:
        conn = sqlite3.connect(str(DB_PATH))
        # Enable row factory to see column names as keys
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print(f"🤖 Running query from {SQL_FILE_PATH.name}...\n")
        cursor.execute(sql_query)
        
        # Check if the query returns data rows (like a SELECT statement)
        rows = cursor.fetchall()
        
        if rows:
            # Dynamically grab the column headers from the result description
            headers = [description[0] for description in cursor.description]
            print(" | ".join(headers))
            print("-" * (len(" | ".join(headers)) + 10))
            
            # Print each data record row
            for row in rows:
                print(" | ".join(str(row[key]) for key in headers))
            print(f"\n✨ Total returned rows: {len(rows)}")
        else:
            conn.commit()
            print("✅ Query executed successfully (No rows returned).")
            
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ SQLite Error: {e}")

if __name__ == "__main__":
    execute_test_query()