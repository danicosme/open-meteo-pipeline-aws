import json
import os

import boto3
from loguru import logger

s3 = boto3.client("s3", region_name=os.getenv("REGION_NAME"))


class S3Service:
    def __init__(self, bucket, key):
        self.bucket = bucket
        self.key = key

    def put_object(self, data):
        try:
            return s3.put_object(
                Body=json.dumps(data),
                Bucket=f"{self.bucket}-processed",
                Key=self.key,
            )
        except Exception as e:
            logger.error(f"An error occurred while putting object: {e}")
            raise e

    def get_object(self):
        try:
            response = s3.get_object(Bucket=self.bucket, Key=self.key)
            return response["Body"].read()
        except Exception as e:
            logger.error(f"An error occurred while getting object: {e}")
            raise e

    def upload_fileobj(self, data, key):
        try:
            s3.upload_fileobj(data, self.bucket, key)
        except Exception as e:
            logger.error(f"An error occurred while uploading file: {e}")
            raise e