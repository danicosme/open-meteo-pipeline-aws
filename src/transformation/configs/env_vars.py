import os

from dotenv import load_dotenv

load_dotenv()

S3_BUCKET = os.getenv("s3_bucket")
