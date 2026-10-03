from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.generator.generate_orders import generate_batch
from src.spark.transform_orders import process_orders_pyspark
from src.analytics import run_analytics
from src.ml.train_churn import train_churn_model

default_args = {
    'owner': 'data_engineering_team',
    'depends_on_past': False,
    'start_date': datetime(2026, 1, 1),
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'ecommerce_data_pipeline_dag',
    default_args=default_args,
    description='Automated Production Data Pipeline with PySpark, SQL, AWS S3 & ML Churn',
    schedule_interval='@daily',
    catchup=False
) as dag:

    task_ingest = PythonOperator(
        task_id='ingest_raw_json_events',
        python_callable=generate_batch,
        op_kwargs={'num_records': 1000, 'output_path': 'raw_orders_sample.json'}
    )

    task_spark_etl = PythonOperator(
        task_id='pyspark_transformation_parquet',
        python_callable=process_orders_pyspark
    )

    task_sql_warehouse = PythonOperator(
        task_id='duckdb_sql_analytics',
        python_callable=run_analytics
    )

    task_ml_churn = PythonOperator(
        task_id='train_customer_churn_model',
        python_callable=train_churn_model
    )

    # Airflow Task Dependency Flow
    task_ingest >> task_spark_etl >> task_sql_warehouse >> task_ml_churn