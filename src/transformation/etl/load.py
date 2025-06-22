import io

import polars as pl
from services.s3 import S3Service


def write_s3(bucket: str, key: str, data):
    return S3Service(bucket=bucket, key=key).put_object(data=data)
