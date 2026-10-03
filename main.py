import logging
import sys
from src.generator.generate_orders import generate_batch
from src.spark.transform_orders import process_orders
from src.analytics import run_analytics

# Force UTF-8 stream encoding for Windows PowerShell terminal
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Configure UTF-8 logging handlers
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
    logging.info("[START] Starting E-commerce Data Pipeline Execution...")
    
    try:
        # Step 1: Ingestion
        logging.info("[Phase 1] Generating raw transactional order batch...")
        generate_batch(num_records=500, output_path="raw_orders_sample.json")
        
        # Step 2: Transformation
        logging.info("[Phase 2] Running ETL process and exporting Parquet...")
        process_orders()
        
        # Step 3: Analytics
        logging.info("[Phase 3] Executing SQL Data Warehouse analytics...")
        run_analytics()
        
        logging.info("[SUCCESS] Pipeline execution finished successfully!")
        
    except Exception as e:
        logging.error(f"[ERROR] Pipeline failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()