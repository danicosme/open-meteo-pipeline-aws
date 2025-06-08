import os

from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("api_url")
S3_BUCKET = os.getenv("s3_bucket")
