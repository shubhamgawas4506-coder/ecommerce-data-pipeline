import duckdb

def run_analytics():
    parquet_path = "output/curated_orders/curated_orders.parquet"
    
    print("==========================================")
    print("📊 1. Total Revenue by Payment Method")
    print("==========================================")
    query_payment = f"""
        SELECT 
            payment_method,
            COUNT(order_id) AS total_orders,
            ROUND(SUM(total_amount), 2) AS total_revenue
        FROM '{parquet_path}'
        WHERE order_status = 'completed'
        GROUP BY payment_method
        ORDER BY total_revenue DESC;
    """
    print(duckdb.sql(query_payment).df().to_string(index=False))
    
    print("\n==========================================")
    print("📈 2. Order Breakdown by Status")
    print("==========================================")
    query_status = f"""
        SELECT 
            order_status,
            COUNT(order_id) AS total_orders,
            ROUND(SUM(total_amount), 2) AS value
        FROM '{parquet_path}'
        GROUP BY order_status
        ORDER BY total_orders DESC;
    """
    print(duckdb.sql(query_status).df().to_string(index=False))

if __name__ == "__main__":
    run_analytics()