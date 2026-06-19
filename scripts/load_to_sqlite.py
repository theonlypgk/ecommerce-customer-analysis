import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "data" / "raw" / "ecommerce_customer_behavior.csv"
DB_PATH  = BASE_DIR / "data" / "ecommerce.db"

df = pd.read_csv(CSV_PATH)

# Normalize column names: lowercase + underscores, safe for SQL
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
)

with sqlite3.connect(DB_PATH) as conn:
    df.to_sql("customers", conn, if_exists="replace", index=False)
    count = conn.execute("SELECT COUNT(*) FROM customers").fetchone()[0]

print(f"OK — {count} rows loaded into '{DB_PATH}'")
print(f"Columns: {list(df.columns)}")
