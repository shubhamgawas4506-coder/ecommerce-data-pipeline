import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import json
import os

def process_orders():
    raw_path = "raw_orders_sample.json"
    output_dir = "output/curated_orders"
    os.makedirs(output_dir, exist_ok=True)

    # Safely load JSON whether array or line-delimited (NDJSON)
    data = []
    with open(raw_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if content.startswith("["):
            data = json.loads(content)
        else:
            data = [json.loads(line) for line in content.splitlines() if line.strip()]

    df = pd.DataFrame(data)
    
    # Data Cleaning & Type Formatting
    df = df.dropna(subset=["order_id"])
    df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)]
    df["order_timestamp"] = pd.to_datetime(df["order_timestamp"])

    # Export to Parquet format
    table = pa.Table.from_pandas(df)
    pq.write_table(table, os.path.join(output_dir, "curated_orders.parquet"))

    print(f"✅ Transformed {len(df)} records into Parquet format!")

if __name__ == "__main__":
    process_orders()