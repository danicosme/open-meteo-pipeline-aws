import polars as pl
from src.processed.services.s3 import S3Service


def read_s3(bucket: str, key: str):
    return S3Service(bucket=bucket, key=key).get_object()


def read_pl_json(file):
    return pl.read_json(file)
