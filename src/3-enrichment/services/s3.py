import os

import boto3
from loguru import logger

s3 = boto3.client("s3", region_name=os.getenv("REGION_NAME"))


class S3Service:
    def __init__(self, bucket, key):
        self.bucket = bucket
        self.key = key

    def get_object(self):
        try:
            response = s3.get_object(Bucket=self.bucket, Key=self.key)
            return response["Body"].read()
        except Exception as e:
            logger.error(f"An error occurred while getting object: {e}")