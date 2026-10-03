from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, dayofmonth, to_timestamp
import os

def process_orders_pyspark():
    # Initialize PySpark Session
    spark = SparkSession.builder \
        .appName("EcommerceSparkETL") \
        .master("local[*]") \
        .getOrCreate()

    raw_path = "raw_orders_sample.json"
    output_dir = "output/curated_orders"

    # 1. Read Raw JSON into PySpark DataFrame
    df = spark.read.json(raw_path)

    # 2. PySpark Data Cleaning & Transformations
    cleaned_df = df.filter(col("order_id").isNotNull()) \
                   .filter((col("quantity") > 0) & (col("unit_price") > 0)) \
                   .withColumn("order_timestamp", to_timestamp(col("order_timestamp"))) \
                   .withColumn("year", year(col("order_timestamp"))) \
                   .withColumn("month", month(col("order_timestamp"))) \
                   .withColumn("day", dayofmonth(col("order_timestamp")))

    # 3. Write Partitioned Parquet Data
    cleaned_df.write \
        .mode("overwrite") \
        .partitionBy("year", "month") \
        .parquet(output_dir)

    print(f"✅ PySpark: Transformed {cleaned_df.count()} records into partitioned Parquet format!")
    spark.stop()

if __name__ == "__main__":
    process_orders_pyspark()