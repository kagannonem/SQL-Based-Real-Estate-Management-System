
-- 1. LEFT JOIN + AGGREGATION + GROUP BY


SELECT 
    a.AgentName,
    COUNT(l.ListingID)      AS total_listings,
    AVG(t.Amount)           AS avg_sale_price
FROM Agents a
LEFT JOIN Listings l     ON a.AgentID = l.AgentID
LEFT JOIN Transactions t ON l.ListingID = t.ListingID
GROUP BY a.AgentName
ORDER BY avg_sale_price DESC;



-- 2. AGGREGATION + GROUP BY + HAVING
--    En az 1 viewing almış listingleri filtrele
--    (HAVING, GROUP BY sonrası filtreleme yapar — WHERE'den farkı bu)


SELECT 
    l.ListingID,
    p.PropertyType,
    p.District,
    COUNT(v.ViewingID) AS total_viewings
FROM Listings l
JOIN Properties p ON l.PropertyID = p.PropertyID
LEFT JOIN Viewings v ON l.ListingID = v.ListingID
GROUP BY l.ListingID, p.PropertyType, p.District
HAVING COUNT(v.ViewingID) >= 1
ORDER BY total_viewings DESC;


-- 3. VIEW — Stale (Uzun Süredir Açık) İlanlar


CREATE VIEW IF NOT EXISTS StaleListings AS
SELECT
    l.ListingID,
    p.PropertyType,
    p.District,
    p.AskingPrice,
    a.AgentName,
    o.OfficeName,
    l.StartDate,
    CAST(JULIANDAY('now') - JULIANDAY(l.StartDate) AS INTEGER) AS days_open
FROM Listings l
JOIN Properties p ON l.PropertyID = p.PropertyID
JOIN Agents a     ON l.AgentID = a.AgentID
JOIN Offices o    ON a.OfficeID = o.OfficeID
WHERE l.Status = 'Active'
  AND CAST(JULIANDAY('now') - JULIANDAY(l.StartDate) AS INTEGER) > 30;

-- View'i kullanmak için:
SELECT * FROM StaleListings;



-- 4. CTE — Agent Viewing-to-Deal Dönüşüm Oranı


WITH AgentViewings AS (
    SELECT
        AgentID,
        COUNT(ViewingID) AS total_viewings
    FROM Viewings
    GROUP BY AgentID
),
AgentDeals AS (
    SELECT
        l.AgentID,
        COUNT(t.TransactionID) AS total_deals
    FROM Transactions t
    JOIN Listings l ON t.ListingID = l.ListingID
    GROUP BY l.AgentID
)
SELECT
    a.AgentName,
    COALESCE(av.total_viewings, 0) AS total_viewings,
    COALESCE(ad.total_deals, 0)    AS total_deals,
    ROUND(
        CAST(COALESCE(ad.total_deals, 0) AS REAL) 
        / NULLIF(av.total_viewings, 0) * 100, 1
    ) AS conversion_rate_pct
FROM Agents a
LEFT JOIN AgentViewings av ON a.AgentID = av.AgentID
LEFT JOIN AgentDeals ad    ON a.AgentID = ad.AgentID
ORDER BY conversion_rate_pct DESC;


-- 5. SELF JOIN — Yönetim Hiyerarşisi
--    Her çalışanın kendi yöneticisiyle eşleştirilmesi.

SELECT
    subordinate.AgentName   AS employee_name,
    subordinate.Level       AS employee_level,
    manager.AgentName       AS reports_to_manager,
    manager.Level           AS manager_level
FROM Agents subordinate
LEFT JOIN Agents manager ON subordinate.ManagerID = manager.AgentID
ORDER BY manager.AgentName, subordinate.AgentName;


-- 6. SUBQUERY — Hiç Satılmamış Mülkler
--    Transactions tablosunda hiç yer almamış listing'lere
--    bağlı mülkleri bul. (NOT IN ile subquery kullanımı)

SELECT
    p.PropertyID,
    p.PropertyType,
    p.District,
    p.AskingPrice,
    p.Status
FROM Properties p
WHERE p.PropertyID NOT IN (
    SELECT l.PropertyID
    FROM Listings l
    JOIN Transactions t ON l.ListingID = t.ListingID
)
ORDER BY p.AskingPrice DESC;


-- 7. SUBQUERY — Ortalamanın Üzerinde Fiyatlı Mülkler
--    Tüm mülklerin ortalama fiyatını subquery ile hesaplayıp
--    bunun üzerindeki mülkleri listele.

SELECT
    PropertyType,
    City,
    District,
    AskingPrice
FROM Properties
WHERE AskingPrice > (
    SELECT AVG(AskingPrice) FROM Properties
)
ORDER BY AskingPrice DESC;
