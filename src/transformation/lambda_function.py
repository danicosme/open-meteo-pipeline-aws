import polars as pl
import boto3
import json

s3 = boto3.client("s3")

def lambda_handler(event, context):
    for record in event.get("Records"):
        body = json.loads(record["body"])

        for body_record in body["Records"]:
            bucket = body_record["s3"]["bucket"]["name"]
            path = body_record["s3"]["object"]["key"]

            json_file = s3.get_object(Bucket=bucket, Key=path)['Body'].read()

            df = pl.read_json(json_file)

            df_hourly = df.select("hourly").unnest("hourly").explode("time", "temperature_2m")
            df_hourly_units = df.select("hourly_units").unnest("hourly_units")

            print(df)


if __name__ == "__main__":
    event = {
  "Records": [
    {
      "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
      "receiptHandle": "MessageReceiptHandle",
      "body": "{\"Records\":[{\"eventVersion\":\"2.1\",\"eventSource\":\"aws:s3\",\"awsRegion\":\"us-east-1\",\"eventTime\":\"2025-06-16T22:00:00.000Z\",\"eventName\":\"ObjectCreated:Put\",\"s3\":{\"s3SchemaVersion\":\"1.0\",\"configurationId\":\"my-s3-to-sqs-config\",\"bucket\":{\"name\":\"open-meteo-pipeline-aws-raw\",\"arn\":\"arn:aws:s3:::open-meteo-pipeline-aws-raw\"},\"object\":{\"key\":\"SP/2025-06-11_1843.json\",\"size\":123456}}}]}",
      "attributes": {
        "ApproximateReceiveCount": "1",
        "SentTimestamp": "1523232000000",
        "SenderId": "123456789012",
        "ApproximateFirstReceiveTimestamp": "1523232000001"
      },
      "messageAttributes": {},
      "md5OfBody": "abcd1234abcd1234abcd1234abcd1234",
      "eventSource": "aws:sqs",
      "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
      "awsRegion": "us-east-1"
    }
  ]
}
    lambda_handler(event, None)