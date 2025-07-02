from unittest.mock import patch
from src.raw.services.s3 import S3Service
import json

bucket = "test-bucket"
key = "state/test.json"
data = {"key": "value"}

@patch('src.raw.services.s3.s3')
def test_put_object_success(mock_s3):
    s3_service = S3Service(bucket)

    s3_service.put_object(data, key)

    mock_s3.put_object.assert_called_once_with(
        Body=json.dumps(data), Bucket=f"{bucket}-raw", Key=key
    )

@patch('src.raw.services.s3.logger')
@patch('src.raw.services.s3.s3')
def test_put_object_fail(mock_s3, mock_logger):
    s3_service = S3Service(bucket)
    mock_s3.put_object.side_effect = Exception("S3 error")

    s3_service.put_object(data, key)

    mock_logger.error.assert_called_once_with("An error occurred: S3 error")
    assert "S3 error" in mock_logger.error.call_args[0][0]