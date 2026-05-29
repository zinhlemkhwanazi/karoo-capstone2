import pandas as pd
import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

# --------------------------------------------------
# Database Connection
# --------------------------------------------------
def get_connection():
    driver = os.getenv("DB_DRIVER", "ODBC Driver 17 for SQL Server")
    server = os.getenv("DB_SERVER")
    database = os.getenv("DB_DATABASE")

    if not server or not database:
        raise RuntimeError("DB_SERVER and DB_DATABASE must be set")

    conn_str = (
        f"DRIVER={driver};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
    )
    return pyodbc.connect(conn_str)


# --------------------------------------------------
# Load CSV Utility
# --------------------------------------------------
def load_csv(csv_path, insert_sql, table_name, columns):
    df = pd.read_csv(csv_path)
    df = df[columns]

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.fast_executemany = True
        cursor.executemany(insert_sql, df.values.tolist())
        conn.commit()
        print(f"✓ Loaded {len(df)} rows into {table_name}")

    except Exception as e:
        conn.rollback()
        print(f"✗ Error loading {table_name}: {e}")

    finally:
        cursor.close()
        conn.close()


# --------------------------------------------------
# Insert Certifications & Harvest Logs
# --------------------------------------------------
def insert_static_data():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Certifications
        cursor.executemany("""
            INSERT INTO Certifications (supplier_id, certification_name, issued_by, issue_date)
            SELECT ?, ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1
                FROM Certifications
                WHERE supplier_id = ? AND certification_name = ?
            )
        """, [
            (1, 'Organic Certified', 'SA Organic', '2024-01-01', 1, 'Organic Certified'),
            (2, 'Fair Trade', 'Fairtrade Africa', '2023-06-15', 2, 'Fair Trade'),
            (3, 'GlobalG.A.P', 'GLOBALG.A.P', '2024-03-10', 3, 'GlobalG.A.P')
        ])

        # Harvest Log
        cursor.executemany("""
            INSERT INTO Harvest_Log (supplier_id, harvest_date, crop_type, quantity_kg)
            VALUES (?, ?, ?, ?)
        """, [
            (1, '2025-10-05', 'Apples', 1200),
            (2, '2025-10-12', 'Grapes', 950),
            (3, '2025-11-01', 'Olives', 700),
            (4, '2025-11-18', 'Grapes', 1300),
            (5, '2025-12-03', 'Olives', 1100)
        ])

        conn.commit()
        print("✓ Certifications and Harvest_Log populated")

    except Exception as e:
        conn.rollback()
        print(f"✗ Error inserting static data: {e}")

    finally:
        cursor.close()
        conn.close()


# --------------------------------------------------
# Main Execution
# --------------------------------------------------
if __name__ == "__main__":

    # Suppliers
    load_csv(
        "suppliers.csv",
        """
        INSERT INTO Suppliers (supplier_id, farm_name, region)
        VALUES (?, ?, ?)
        """,
        "Suppliers",
        ["supplier_id", "farm_name", "region"]
    )

    # Orders (matches CSV & schema)
    load_csv(
        "orders.csv",
        """
        INSERT INTO Orders (order_id, supplier_id, order_date, total_price)
        VALUES (?, ?, ?, ?)
        """,
        "Orders",
        ["order_id", "supplier_id", "order_date", "total_price"]
    )

    # Sales Targets
    load_csv(
        "targets.csv",
        """
        INSERT INTO Sales_Targets (region, quarter, target_amount)
        VALUES (?, ?, ?)
        """,
        "Sales_Targets",
        ["region", "quarter", "target_amount"]
    )

    # Static data
    insert_static_data()

    print("\n✓ All tables populated successfully.")
