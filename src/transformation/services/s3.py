import json
import os

import awswrangler as wr
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
            raise e

    def write_parquet(self, df, partition_cols):
        try:
            wr.s3.to_parquet(
                df=df,
                path=f"s3://{self.bucket}/{self.key}",
                dataset=True,
                mode="overwrite_partitions",
                partition_cols=partition_cols,
            )
        except Exception as e:
            logger.error(f"An error occurred while writing parquet: {e}")
            raise e
