import pandas as pd
import duckdb
import os

def process_orders():
    raw_path = "raw_orders_sample.json"
    output_dir = "output/curated_orders"
    
    # 1. Read Raw JSON into Pandas
    df = pd.read_json(raw_path, lines=True)
    
    # 2. Data Cleaning & Schema Transformation
    df = df.dropna(subset=["order_id"])
    df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)]
    
    df["order_timestamp"] = pd.to_datetime(df["order_timestamp"])
    df["year"] = df["order_timestamp"].dt.year
    df["month"] = df["order_timestamp"].dt.month
    df["day"] = df["order_timestamp"].dt.day
    
    # 3. Export to Parquet format
    os.makedirs(output_dir, exist_ok=True)
    df.to_parquet(os.path.join(output_dir, "curated_orders.parquet"), index=False)
    
    print(f"✅ Successfully transformed {len(df)} records into Parquet format!")

if __name__ == "__main__":
    process_orders()