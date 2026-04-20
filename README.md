# SQL Based Real Estate Management System team27
MTM4692 - Applied SQL Project: For this project, our group is designing and implementing a relational database for a real estate agency. So far we have completed the ER diagram and project report. The database will handle property listings, agents, offices, clients, viewings, and transactions.

Below you can view the ER diagram for the project.

<img width="3186" height="1344" alt="ER" src="https://github.com/user-attachments/assets/6179ce79-aa3b-4810-9e4b-a674d287c179" />

# Key Relationships

- `Agents.OfficeID` → `Offices.OfficeID`
- `Agents.ManagerID` → `Agents.AgentID` *(self-referencing)*
- `Listing.PropertyID` → `Properties.PropertyID`
- `Listing.OwnerID` → `Clients.ClientID`
- `Viewings.ListingID` → `Listing.ListingID`
- `Viewings.ClientID` → `Clients.ClientID`
- `Transactions.ListingID` → `Listing.ListingID`
- `Transactions.BuyerID` → `Clients.ClientID`

The following diagram illustrates the entity-relationship structure of the Real Estate Management System, showing the seven core tables and their associations.

<img width="749" height="557" alt="table" src="https://github.com/user-attachments/assets/0a3e6acb-4a78-45d4-80c8-232f85afb15e" />
