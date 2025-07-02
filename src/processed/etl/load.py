import polars as pl
from services.s3 import S3Service


def write_s3(df: pl.DataFrame, bucket: str, key: str, partition_cols: list):
    return S3Service(bucket=bucket, key=key).write_parquet(
        df=df,  partition_cols=partition_cols
    )
