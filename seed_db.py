import sqlite3
from pathlib import Path

PROJECT_DIR = Path(__file__).parent.resolve()
DB_PATH = PROJECT_DIR / "real_estate.db"

def seed_database():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()
    
    print("Seeding data into real_estate.db...")

    # 1. Insert Offices
    offices_data = [
        ('Kadıköy Branch', 'İstanbul', 'Kadıköy', '+902165551122', 'kadikoy@agency.com'),
        ('Beşiktaş Branch', 'İstanbul', 'Beşiktaş', '+902125553344', 'besiktas@agency.com'),
        ('Fatih Branch', 'İstanbul', 'Fatih', '+902125555566', 'fatih@agency.com')
    ]
    cursor.executemany("""
        INSERT INTO Offices (OfficeName, City, District, PhoneNumber, Email) 
        VALUES (?, ?, ?, ?, ?);
    """, offices_data)
    
    # 2. Insert Agents (Building an organizational hierarchy)
    # Principal Director (No Manager)
    cursor.execute("""
        INSERT INTO Agents (OfficeID, AgentName, Email, ManagerID, Level) 
        VALUES (1, 'Suna Seyrek', 'suna@agency.com', NULL, 'Director');
    """)
    director_id = cursor.lastrowid

    # Mid-level Manager (Reports to Director)
    cursor.execute("""
        INSERT INTO Agents (OfficeID, AgentName, Email, ManagerID, Level) 
        VALUES (1, 'Ece Naz Özbucak', 'ece@agency.com', ?, 'Manager');
    """, (director_id,))
    manager_id = cursor.lastrowid

    # Junior Agent (Reports to Manager)
    cursor.execute("""
        INSERT INTO Agents (OfficeID, AgentName, Email, ManagerID, Level) 
        VALUES (1, 'Zekiye Miray Karagöz', 'miray@agency.com', ?, 'Junior');
    """, (manager_id,))
    
    # Independent Agent in another office
    cursor.execute("""
        INSERT INTO Agents (OfficeID, AgentName, Email, ManagerID, Level) 
        VALUES (2, 'John Doe', 'john@agency.com', NULL, 'Senior Agent');
    """)

    # 3. Insert Clients (Sellers and Buyers)
    clients_data = [
        ('Ahmet Yılmaz', '+905321112233', 'ahmet@mail.com', 'Seller', '2026-01-15'),
        ('Ayşe Demir', '+905334445566', 'ayse@mail.com', 'Buyer', '2026-02-10'),
        ('Mehmet Kaya', '+905427778899', 'mehmet@mail.com', 'Both', '2026-03-01'),
        ('Fatma Şahin', '+905559990011', 'fatma@mail.com', 'Buyer', '2026-04-12')
    ]
    cursor.executemany("""
        INSERT INTO Clients (ClientName, ClientPhone, ClientMail, ClientType, RegDate) 
        VALUES (?, ?, ?, ?, ?);
    """, clients_data)

    # 4. Insert Properties
    properties_data = [
        ('Apartment', 'İstanbul', 'Kadıköy', 120.0, 4500000.0, 'Available'),
        ('Villa', 'İstanbul', 'Beşiktaş', 350.0, 18500000.0, 'Available'),
        ('Studio', 'İstanbul', 'Fatih', 55.0, 2200000.0, 'Available'),
        ('Office Space', 'İstanbul', 'Kadıköy', 85.0, 3800000.0, 'Available')
    ]
    cursor.executemany("""
        INSERT INTO Properties (PropertyType, City, District, Area, AskingPrice, Status) 
        VALUES (?, ?, ?, ?, ?, ?);
    """, properties_data)

    # 5. Insert Listings
    # Linking Property 1, Agent 3 (Junior), Owner 1 (Ahmet)
    # Linking Property 2, Agent 2 (Manager), Owner 3 (Mehmet)
    listings_data = [
        (1, 3, 1, '2026-01-20', None, 4400000.0, 'Active'),
        (2, 2, 3, '2026-02-15', None, 18000000.0, 'Active'),
        (3, 4, 1, '2026-03-10', '2026-05-20', 21500000.0, 'Closed')
    ]
    cursor.executemany("""
        INSERT INTO Listings (PropertyID, AgentID, OwnerID, StartDate, EndDate, ListingPrice, Status) 
        VALUES (?, ?, ?, ?, ?, ?, ?);
    """, listings_data)

    # 6. Insert Viewings
    viewings_data = [
        (1, 2, 3, '2026-01-25', 'Client loved the balcony view, considering an offer.'),
        (1, 4, 3, '2026-02-02', 'Budget constraints, client found price high.'),
        (2, 2, 2, '2026-02-20', 'Requested a second viewing with family.')
    ]
    cursor.executemany("""
        INSERT INTO Viewings (ListingID, ClientID, AgentID, ViewingDate, Feedback) 
        VALUES (?, ?, ?, ?, ?);
    """, viewings_data)

    # 7. Insert Transactions (Closing a deal)
    # Listing 3 sold to Buyer 2 (Ayşe) by Agent 4 (John)
    cursor.execute("""
        INSERT INTO Transactions (ListingID, BuyerID, AgentID, Amount, TransactionDate) 
        VALUES (3, 2, 4, 21000000.0, '2026-05-20');
    """)
    
    # Update property status to reflect sale
    cursor.execute("UPDATE Properties SET Status = 'Sold' WHERE PropertyID = 3;")

    conn.commit()
    conn.close()
    print("🏁 Database mock seeding complete!")

if __name__ == "__main__":
    seed_database()