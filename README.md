# Real Estate Management System

A normalized relational database with a fully working web application, built for a multi-office real estate agency.

**Yıldız Technical University — MTM4962 Final Project**  
Efe Kağan Önem · Ece Naz Özbucak · Suna Seyrek · Zekiye Miray Karagöz

---

## Tech Stack

- **Backend:** Python, FastAPI
- **Database:** SQLite
- **Frontend:** HTML, CSS, JavaScript

## Database Schema

7 normalized tables: `Offices`, `Agents`, `Clients`, `Properties`, `Listings`, `Viewings`, `Transactions`

Key design decisions:
- Agents table has a self-referencing foreign key (`ManagerID`) to model the management hierarchy
- Clients table has a `CHECK` constraint on `ClientType` (Buyer / Seller / Both)
- Recording a transaction automatically sets the listing to `Closed` and the property to `Sold`

## SQL Features

- `JOIN`, `LEFT JOIN`, `Self JOIN`
- `GROUP BY`, `HAVING`, `AVG`, `SUM`, `COUNT`
- `VIEW` (StaleListings — listings open for 30+ days)
- `CTE` (agent viewing-to-deal conversion rate)
- Subqueries (`NOT IN`, scalar subquery)

## Project Structure

```
├── app.py
├── setup_db.py
├── seed_db.py
├── real_estate.db
├── index.html
├── sampleQueries.sql
└── dao/
    ├── agent_dao.py
    ├── property_dao.py
    ├── client_dao.py
    ├── listing_dao.py
    ├── viewing_dao.py
    ├── transaction_dao.py
    └── office_dao.py
```
