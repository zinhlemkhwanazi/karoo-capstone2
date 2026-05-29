/* =========================================================
   Q4 2025 Regional Performance vs Targets
   ========================================================= */

-- 1. Region, Actual Revenue, Target Amount, % of Target
SELECT
    s.region,
    SUM(o.total_price) AS actual_revenue,
    t.target_amount,
    CASE
        WHEN t.target_amount = 0 THEN 0
        ELSE ROUND((SUM(o.total_price) / t.target_amount) * 100, 2)
    END AS percent_of_target
FROM Orders o
JOIN Suppliers s
    ON o.supplier_id = s.supplier_id
JOIN Sales_Targets t
    ON s.region = t.region
WHERE t.quarter = '2025-Q4'
GROUP BY s.region, t.target_amount
ORDER BY s.region;


/* =========================================================
   Top 3 Suppliers per Region by Revenue (Q4 2025)
   ========================================================= */

SELECT
    region,
    supplier_id,
    farm_name,
    revenue,
    supplier_rank
FROM (
    SELECT
        s.region,
        s.supplier_id,
        s.farm_name,
        SUM(o.total_price) AS revenue,
        RANK() OVER (
            PARTITION BY s.region
            ORDER BY SUM(o.total_price) DESC
        ) AS supplier_rank
    FROM Orders o
    JOIN Suppliers s
        ON o.supplier_id = s.supplier_id
    WHERE o.order_date BETWEEN '2025-10-01' AND '2025-12-31'
    GROUP BY s.region, s.supplier_id, s.farm_name
) ranked_suppliers
WHERE supplier_rank <= 3
ORDER BY region, supplier_rank;
