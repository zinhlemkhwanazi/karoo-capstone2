import pandas as pd
import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()

# --------------------------------------------------
# Database Connection
# --------------------------------------------------
def get_connection():
    conn_str = (
        f"DRIVER={os.getenv('DB_DRIVER')};"
        f"SERVER={os.getenv('DB_SERVER')};"
        f"DATABASE={os.getenv('DB_DATABASE')};"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)


# --------------------------------------------------
# Main Report Generator
# --------------------------------------------------
def generate_q4_report():
    conn = None
    try:
        conn = get_connection()

        # Query 1: Regional Performance vs Target
        regional_query = """
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
        """

        regional_df = pd.read_sql(regional_query, conn)

        # Query 2: Top 3 Suppliers per Region
        supplier_query = """
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
        ) ranked
        WHERE supplier_rank <= 3
        """

        suppliers_df = pd.read_sql(supplier_query, conn)

        # Save outputs
        regional_df.to_csv("q4_performance.csv", index=False)
        suppliers_df.to_csv("q4_top_suppliers.csv", index=False)

        # Console Summary
        print("\n=== Q4 2025 Regional Performance ===")
        print(regional_df)

        print("\n=== Top 3 Suppliers per Region ===")
        print(suppliers_df)

        print("\n✓ Q4 reports generated successfully.")

    except Exception as e:
        print(f"✗ Error generating Q4 report: {e}")

    finally:
        if conn:
            conn.close()


# --------------------------------------------------
# Run Script
# --------------------------------------------------
if __name__ == "__main__":
    generate_q4_report()
