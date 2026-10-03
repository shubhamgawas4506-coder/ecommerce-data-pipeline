import duckdb
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def train_churn_model():
    parquet_path = "output/curated_orders/curated_orders.parquet"
    
    # Feature Engineering: Extract Customer-Level RFM Metrics using DuckDB
    query = f"""
        WITH customer_summary AS (
            SELECT 
                customer_id,
                MAX(order_timestamp) AS last_order_date,
                COUNT(order_id) AS frequency,
                SUM(CASE WHEN order_status = 'completed' THEN total_amount ELSE 0 END) AS total_spend,
                AVG(total_amount) AS avg_order_value,
                SUM(CASE WHEN order_status = 'cancelled' THEN 1 ELSE 0 END) AS cancelled_orders
            FROM '{parquet_path}'
            GROUP BY customer_id
        ),
        max_date_cte AS (
            SELECT MAX(order_timestamp) AS global_max_date FROM '{parquet_path}'
        )
        SELECT 
            cs.customer_id,
            DATEDIFF('day', cs.last_order_date, md.global_max_date) AS recency_days,
            cs.frequency,
            cs.total_spend,
            cs.avg_order_value,
            cs.cancelled_orders,
            CASE 
                WHEN DATEDIFF('day', cs.last_order_date, md.global_max_date) > 12 
                     OR (cs.cancelled_orders * 1.0 / cs.frequency) >= 0.3 THEN 1 
                ELSE 0 
            END AS is_churn
        FROM customer_summary cs, max_date_cte md;
    """
    
    df = duckdb.sql(query).df()
    
    if len(df) < 20:
        print("[ML] Not enough customer records to train churn model.")
        return

    features = ['recency_days', 'frequency', 'total_spend', 'avg_order_value', 'cancelled_orders']
    X = df[features]
    y = df['is_churn']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    
    print("==========================================")
    print("🤖 E-Commerce Customer Churn Model Results")
    print("==========================================")
    print(f"Total Customers Analyzed: {len(df)}")
    print(f"Total Churned Customers:  {y.sum()} ({(y.sum()/len(df))*100:.1f}%)")
    print(f"Accuracy:                 {accuracy_score(y_test, y_pred)*100:.2f}%")
    print(f"Precision:                {precision_score(y_test, y_pred, zero_division=0):.2f}")
    print(f"Recall:                   {recall_score(y_test, y_pred, zero_division=0):.2f}")
    print(f"F1-Score:                 {f1_score(y_test, y_pred, zero_division=0):.2f}")

if __name__ == "__main__":
    train_churn_model()