import io

import polars as pl

from src.common.services.s3 import S3Service


def pl_read_parquet_from_s3(bucket, key):
    s3_service = S3Service(bucket=bucket, key=key)
    response = s3_service.get_object()
    return pl.read_parquet(io.BytesIO(response))
