import logging
import sys
from src.generator.generate_orders import generate_batch
from src.spark.transform_orders import process_orders
from src.analytics import run_analytics
from src.ml.train_churn import train_churn_model

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

file_handler = logging.FileHandler("pipeline.log", encoding="utf-8")
file_handler.setFormatter(formatter)

logger.handlers.clear()
logger.addHandler(stream_handler)
logger.addHandler(file_handler)

def run_pipeline():
    logging.info("[START] Starting E-commerce Data & ML Churn Pipeline...")
    
    try:
        logging.info("[Phase 1] Generating raw transactional order batch...")
        generate_batch(num_records=1000, output_path="raw_orders_sample.json")
        
        logging.info("[Phase 2] Running ETL process and exporting Parquet...")
        process_orders()
        
        logging.info("[Phase 3] Executing SQL Data Warehouse analytics...")
        run_analytics()
        
        logging.info("[Phase 4] Training Customer Churn ML Model...")
        train_churn_model()
        
        logging.info("[SUCCESS] Complete End-to-End Pipeline execution finished!")
        
    except Exception as e:
        logging.error(f"[ERROR] Pipeline failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()