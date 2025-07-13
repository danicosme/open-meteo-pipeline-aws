import pytest

from unittest.mock import patch
from src.processed.services.s3 import S3Service

bucket = "test-bucket"
key = "state/test.json"
df = {"col1": [1, 2], "col2": [3, 4]}
partition_cols = ["col1"]

@pytest.fixture
def s3_service():   
    return S3Service(bucket, key)

@patch('src.processed.services.s3.s3')
def test_get_object_success(mock_s3, s3_service):
    s3_service.get_object()

    mock_s3.get_object.assert_called_once_with(
        Bucket=bucket, Key=key
    )

@patch('src.processed.services.s3.logger')
@patch('src.processed.services.s3.s3')
def test_get_object_fail(mock_s3, mock_logger, s3_service):
    mock_s3.get_object.side_effect = Exception("S3 error")

    s3_service.get_object()

    mock_logger.error.assert_called_once_with("An error occurred while getting object: S3 error")
    assert "S3 error" in mock_logger.error.call_args[0][0]


@patch('src.processed.services.s3.wr')
def test_write_parquet_partitioned_success(mock_wr, s3_service):
    s3_service.write_parquet_partitioned(df, partition_cols)

    mock_wr.s3.to_parquet.assert_called_once_with(
        df=df,
        path=f"s3://{bucket}/{key}",
        dataset=True,
        mode="overwrite_partitions",
        partition_cols=partition_cols,
    )

@patch('src.processed.services.s3.logger')
@patch('src.processed.services.s3.wr')  
def test_write_parquet_partitioned_fail(mock_wr, mock_logger, s3_service):
    mock_wr.s3.to_parquet.side_effect = Exception("S3 error")

    s3_service.write_parquet_partitioned(df, partition_cols)

    mock_logger.error.assert_called_once_with("An error occurred while writing parquet: S3 error")
    assert "S3 error" in mock_logger.error.call_args[0][0]


@patch('src.processed.services.s3.wr')
def test_write_parquet_success(mock_wr, s3_service):
    s3_service.write_parquet(df)

    mock_wr.s3.to_parquet.assert_called_once_with(
        df=df,
        path=f"s3://{bucket}/{key}",
        dataset=True,
        mode="overwrite",
    )