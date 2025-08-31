import json

from job import run_job
from loguru import logger


def lambda_handler(event, context):
    records = event.get("Records", [])
    if not records:
        logger.error("Nenhum registro encontrado no evento.")
        return
    for record in records:
        try:
            body = json.loads(record["body"])
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"Erro ao decodificar body do record: {e}. Record: {record}")
            continue
        for body_record in body.get("Records", []):
            run_job(body_record)


if __name__ == "__main__":
    event = {
        "Records": [
            {
                "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
                "receiptHandle": "MessageReceiptHandle",
                "body": '{"Records":[{"eventVersion":"2.1","eventSource":"aws:s3","awsRegion":"us-east-1","eventTime":"2025-06-16T22:00:00.000Z","eventName":"ObjectCreated:Put","s3":{"s3SchemaVersion":"1.0","configurationId":"my-s3-to-sqs-config","bucket":{"name":"open-meteo-pipeline-aws-raw","arn":"arn:aws:s3:::open-meteo-pipeline-aws-raw"},"object":{"key":"2025-07-06T12-06-18/SP_sao_paulo.json","size":123456}}}]}',
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
            },
            {
                "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
                "receiptHandle": "MessageReceiptHandle",
                "body": '{"Records":[{"eventVersion":"2.1","eventSource":"aws:s3","awsRegion":"us-east-1","eventTime":"2025-06-16T22:00:00.000Z","eventName":"ObjectCreated:Put","s3":{"s3SchemaVersion":"1.0","configurationId":"my-s3-to-sqs-config","bucket":{"name":"open-meteo-pipeline-aws-raw","arn":"arn:aws:s3:::open-meteo-pipeline-aws-raw"},"object":{"key":"2025-07-06T12-06-18/SC_florianopolis.json","size":123456}}}]}',
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
            },
        ]
    }
    lambda_handler(event, None)
