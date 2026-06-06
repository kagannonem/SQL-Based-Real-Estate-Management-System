import sqlite3
from pathlib import Path

# Pinpoint the exact folder where this setup_db.py file lives
PROJECT_DIR = Path(__file__).parent.resolve()
DB_PATH = PROJECT_DIR / "real_estate.db"

def initialize_database():
    # Establish connection and force SQLite to strictly respect your EER rules
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON;")
    
    schema_sql = """
    -- 1. OFFICES TABLE
    CREATE TABLE IF NOT EXISTS Offices (
        OfficeID INTEGER PRIMARY KEY AUTOINCREMENT,
        OfficeName TEXT NOT NULL,
        City TEXT NOT NULL,
        District TEXT NOT NULL,
        PhoneNumber TEXT,
        Email TEXT
    );

    -- 2. AGENTS TABLE (With Self-Referencing Manager ID)
    CREATE TABLE IF NOT EXISTS Agents (
        AgentID INTEGER PRIMARY KEY AUTOINCREMENT,
        OfficeID INTEGER,
        AgentName TEXT NOT NULL,
        Email TEXT UNIQUE,
        ManagerID INTEGER,
        Level TEXT,
        FOREIGN KEY (OfficeID) REFERENCES Offices(OfficeID) ON DELETE SET NULL,
        FOREIGN KEY (ManagerID) REFERENCES Agents(AgentID) ON DELETE SET NULL
    );

    -- 3. CLIENTS TABLE
    CREATE TABLE IF NOT EXISTS Clients (
        ClientID INTEGER PRIMARY KEY AUTOINCREMENT,
        ClientName TEXT NOT NULL,
        ClientPhone TEXT,
        ClientMail TEXT UNIQUE,
        ClientType TEXT CHECK(ClientType IN ('Buyer', 'Seller', 'Both')),
        RegDate TEXT DEFAULT (date('now'))
    );

    -- 4. PROPERTIES TABLE
    CREATE TABLE IF NOT EXISTS Properties (
        PropertyID INTEGER PRIMARY KEY AUTOINCREMENT,
        PropertyType TEXT NOT NULL,
        City TEXT NOT NULL,
        District TEXT NOT NULL,
        Area REAL,
        AskingPrice REAL,
        Status TEXT DEFAULT 'Available'
    );

    -- 5. LISTINGS TABLE
    CREATE TABLE IF NOT EXISTS Listings (
        ListingID INTEGER PRIMARY KEY AUTOINCREMENT,
        PropertyID INTEGER NOT NULL,
        AgentID INTEGER NOT NULL,
        OwnerID INTEGER NOT NULL,
        StartDate TEXT NOT NULL,
        EndDate TEXT,
        ListingPrice REAL NOT NULL,
        Status TEXT DEFAULT 'Active',
        FOREIGN KEY (PropertyID) REFERENCES Properties(PropertyID) ON DELETE CASCADE,
        FOREIGN KEY (AgentID) REFERENCES Agents(AgentID) ON DELETE RESTRICT,
        FOREIGN KEY (OwnerID) REFERENCES Clients(ClientID) ON DELETE RESTRICT
    );

    -- 6. VIEWINGS TABLE
    CREATE TABLE IF NOT EXISTS Viewings (
        ViewingID INTEGER PRIMARY KEY AUTOINCREMENT,
        ListingID INTEGER NOT NULL,
        ClientID INTEGER NOT NULL,
        AgentID INTEGER NOT NULL,
        ViewingDate TEXT NOT NULL,
        Feedback TEXT,
        FOREIGN KEY (ListingID) REFERENCES Listings(ListingID) ON DELETE CASCADE,
        FOREIGN KEY (ClientID) REFERENCES Clients(ClientID) ON DELETE CASCADE,
        FOREIGN KEY (AgentID) REFERENCES Agents(AgentID) ON DELETE RESTRICT
    );

    -- 7. TRANSACTIONS TABLE
    CREATE TABLE IF NOT EXISTS Transactions (
        TransactionID INTEGER PRIMARY KEY AUTOINCREMENT,
        ListingID INTEGER NOT NULL,
        BuyerID INTEGER NOT NULL,
        AgentID INTEGER NOT NULL,
        Amount REAL NOT NULL,
        TransactionDate TEXT NOT NULL,
        FOREIGN KEY (ListingID) REFERENCES Listings(ListingID) ON DELETE RESTRICT,
        FOREIGN KEY (BuyerID) REFERENCES Clients(ClientID) ON DELETE RESTRICT,
        FOREIGN KEY (AgentID) REFERENCES Agents(AgentID) ON DELETE RESTRICT
    );
    """
    
    print("Creating tables...")
    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    
    print("\n================ SUCCESS ================")
    print(f"Database fully generated at: {DB_PATH}")
    print("=========================================\n")

if __name__ == "__main__":
    initialize_database()