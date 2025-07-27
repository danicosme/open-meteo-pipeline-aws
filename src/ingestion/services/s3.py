import json
import os

import boto3
from loguru import logger

s3 = boto3.client("s3", region_name=os.getenv("REGION_NAME"))


class S3Service:
    def __init__(self, s3_bucket):
        self.s3_bucket = s3_bucket

    def put_object(self, data, key):
        try:
            s3.put_object(
                Body=json.dumps(data), Bucket=f"{self.s3_bucket}-raw", Key=key
            )
        except Exception as e:
            logger.error(f"An error occurred: {e}")
