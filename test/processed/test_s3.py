from unittest.mock import patch
from src.processed.services.s3 import S3Service
import json

bucket = "test-bucket"
key = "state/test.json"
data = {"key": "value"}

@patch('src.processed.services.s3.s3')
def test_get_object_success(mock_s3):
    s3_service = S3Service(bucket, key)

    s3_service.get_object()

    mock_s3.get_object.assert_called_once_with(
        Bucket=bucket, Key=key
    )