import json

from etl import extract, load, transform
from loguru import logger
from schema.column_mapping import (
    weather_columns,
    weather_columns_hourly,
    weather_columns_hourly_units,
)


def lambda_handler(event, context):
    for record in event.get("Records"):
        body = json.loads(record["body"])

        for body_record in body["Records"]:
            bucket = body_record["s3"]["bucket"]["name"]
            path = body_record["s3"]["object"]["key"]

            # Extract
            json_file = extract.read_s3(bucket=bucket, key=path)
            df_weather = extract.read_pl_json(file=json_file)

            # Transform
            df_weather_hourly = transform.pl_unnest_explode(
                df=df_weather,
                columns=["latitude", "longitude", "hourly", "extraction_datetime"],
                unnest_column="hourly",
                explode_columns=["time", "temperature_2m"],
            )
            df_weather_hourly_units = transform.pl_unnest(
                df=df_weather,
                columns=[
                    "latitude",
                    "longitude",
                    "hourly_units",
                    "extraction_datetime",
                ],
                unnest_column="hourly_units",
            )

            df_weather = transform.pl_drop_columns(
                df_weather, ["hourly", "hourly_units"]
            )

            df_weather = transform.pl_cast(df_weather, weather_columns)
            df_weather_hourly = transform.pl_cast(
                df_weather_hourly, weather_columns_hourly
            )
            df_weather_hourly_units = transform.pl_cast(
                df_weather_hourly_units, weather_columns_hourly_units
            )

            # Load


if __name__ == "__main__":
    event = {
        "Records": [
            {
                "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
                "receiptHandle": "MessageReceiptHandle",
                "body": '{"Records":[{"eventVersion":"2.1","eventSource":"aws:s3","awsRegion":"us-east-1","eventTime":"2025-06-16T22:00:00.000Z","eventName":"ObjectCreated:Put","s3":{"s3SchemaVersion":"1.0","configurationId":"my-s3-to-sqs-config","bucket":{"name":"open-meteo-pipeline-aws-raw","arn":"arn:aws:s3:::open-meteo-pipeline-aws-raw"},"object":{"key":"SP/2025-06-11_1843.json","size":123456}}}]}',
                "attributes": {
                    "ApproximateReceiveCount": "1",
                    "SentTimestamp": "1523232000000",
                    "SenderId": "123456789012",
                    "ApproximateFirstReceiveTimestamp": "1523232000001",
                },
                "messageAttributes": {},
                "md5OfBody": "abcd1234abcd1234abcd1234abcd1234",
                "eventSource": "aws:sqs",
                "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
                "awsRegion": "us-east-1",
            }
        ]
    }
    lambda_handler(event, None)
