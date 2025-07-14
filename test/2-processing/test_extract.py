import io
import polars as pl

from unittest.mock import patch
from src.processed.etl.extract import read_s3, read_pl_json

bucket = "test-bucket"
key = "test-key"
data = '{"key": "value"}'

@patch("src.processed.services.s3.S3Service.get_object")
def test_read_success(mock_get_object):
    mock_get_object.return_value = data
    result = read_s3(bucket, key)
    assert result == data

@patch("src.processed.services.s3.S3Service.get_object")
def test_read_fail(mock_get_object):
    mock_get_object.side_effect = Exception("S3 read error")
    try:
        read_s3(bucket, key)
    except Exception as e:
        assert str(e) == "S3 read error"

def test_read_pl_json():
    json_file = io.StringIO(data)
    df = read_pl_json(json_file)

    assert isinstance(df, pl.DataFrame)
    assert df.shape == (1, 1)

def test_read_pl_json_invalid():
    json_file = io.StringIO("json")
    try:
        read_pl_json(json_file)
    except Exception as e:
        assert "InternalError" in str(e)