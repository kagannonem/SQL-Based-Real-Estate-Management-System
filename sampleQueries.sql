

-- Sample Query with Aggregation, LEFT JOIN and GROUP BY
-- This query returns each agent's total number of listings 
-- and the average sale price of their closed transactions.

SELECT a.agent_name,
       COUNT(l.listing_id) AS total_listings,
       AVG(t.transaction_amount) AS avg_sale_price
FROM agent a
LEFT JOIN listing l ON a.agent_id = l.agent_id
LEFT JOIN [transaction] t ON l.listing_id = t.listing_id
GROUP BY a.agent_name
ORDER BY avg_sale_price DESC;

-- Sample Query with VIEW, JULIANDAY
-- This view returns all active listings that have been open
-- for more than 30 days. These are considered "stale" 
-- and may show a pricing issue or lack of agent attention.

CREATE VIEW StaleListings AS
SELECT
    l.listing_id,
    p.type AS property_type,
    p.district,
    p.asking_price,
    a.agent_name,
    o.office_name,
    l.start_date,
    CAST(JULIANDAY('now') - JULIANDAY(l.start_date) AS INTEGER) AS days_open
FROM listing l
JOIN properties p ON l.property_id = p.property_id
JOIN agents a ON l.agent_id = a.agent_id
JOIN offices o ON a.office_id = o.office_id
WHERE l.status = 'active'
  AND CAST(JULIANDAY('now') - JULIANDAY(l.start_date) AS INTEGER) > 30;

-- Sample Query with CTEs, Aggregations.
-- This query calculates each agent's viewing-to-deal conversion rate.
-- Two separate CTEs are used to count viewings and closed deals
-- independently, then joined together to compute the final ratio.

WITH AgentViewings AS (
    SELECT
        agent_id,
        COUNT(viewing_id) AS total_viewings
    FROM viewings
    GROUP BY agent_id
),
AgentDeals AS (
    SELECT
        l.agent_id,
        COUNT(t.transaction_id) AS total_deals
    FROM transactions t
    JOIN listing l ON t.listing_id = l.listing_id
    GROUP BY l.agent_id
)
SELECT
    a.agent_name,
    av.total_viewings,
    ad.total_deals,
    ROUND(
        CAST(ad.total_deals AS REAL) / av.total_viewings * 100, 1
    ) AS conversion_rate
FROM agents a
JOIN AgentViewings av   ON a.agent_id = av.agent_id
LEFT JOIN AgentDeals ad ON a.agent_id = ad.agent_id
ORDER BY conversion_rate DESC;