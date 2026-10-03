import boto3
import os
from botocore.exceptions import NoCredentialsError

def upload_to_s3(local_file_path, bucket_name, s3_key):
    """
    Uploads local JSON or Parquet pipeline artifacts to an AWS S3 Bucket.
    """
    s3 = boto3.client('s3')
    try:
        s3.upload_file(local_file_path, bucket_name, s3_key)
        print(f"☁️ AWS S3: Successfully uploaded {local_file_path} to s3://{bucket_name}/{s3_key}")
    except NoCredentialsError:
        print("⚠️ AWS Credentials not found. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.")
    except Exception as e:
        print(f"❌ S3 Upload Failed: {str(e)}")

if __name__ == "__main__":
    # Example usage
    upload_to_s3("raw_orders_sample.json", "my-ecommerce-data-lake", "raw/orders.json")