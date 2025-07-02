import json

from etl import extract, load, transform
from loguru import logger
from schema.column_mapping import (
    weather_columns,
    weather_columns_hourly,
    weather_columns_hourly_units,
)
from configs.env_vars import S3_BUCKET


def run_job(body_record):
    # Extract
    try:
        bucket = body_record["s3"]["bucket"]["name"]
        path = body_record["s3"]["object"]["key"]
    except KeyError as e:
        logger.error(f"Chave ausente no registro S3: {e}. Registro: {body_record}")
        return

    logger.info(f"Processing file: s3://{bucket}/{path}")
    try:
        json_file = extract.read_s3(bucket=bucket, key=path)
        df_weather = extract.read_pl_json(file=json_file)
    except Exception as e:
        logger.error(f"Erro ao extrair arquivo {path} do bucket {bucket}: {e}")
        return

    # Transform
    try:
        logger.info("Transforming dataframes")
        df_weather_hourly = transform.pl_unnest_explode(
            df=df_weather,
            columns=["latitude", "longitude", "state", "hourly", "extraction_datetime"],
            unnest_column="hourly",
            explode_columns=["time", "temperature_2m"],
        )
        df_weather_hourly_units = transform.pl_unnest(
            df=df_weather,
            columns=[
                "latitude",
                "longitude",
                "state",
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
        df_weather_hourly = transform.pl_create_partition(
            df=df_weather_hourly, time_col="time"
        )
    except Exception as e:
        logger.error(f"Erro na transformação do arquivo {path}: {e}")
        return

    # Load
    try:
        logger.info("Loading dataframes to S3")
        df_weather = df_weather.to_pandas()
        df_weather_hourly = df_weather_hourly.to_pandas()
        df_weather_hourly_units = df_weather_hourly_units.to_pandas()
        load.write_s3(
            df=df_weather,
            bucket=f"{S3_BUCKET}-processed",
            key="df_weather",
            partition_cols=["state"],
        )
        load.write_s3(
            df=df_weather_hourly,
            bucket=f"{S3_BUCKET}-processed",
            key="df_weather_hourly",
            partition_cols=["state", "year", "month", "day", "hour"],
        )
        load.write_s3(
            df=df_weather_hourly_units,
            bucket=f"{S3_BUCKET}-processed",
            key="df_weather_hourly_units",
            partition_cols=["state"],
        )
        logger.info(f"Arquivo {path} processado e salvo com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao salvar dados processados do arquivo {path}: {e}")


def lambda_handler(event, context):
    records = event.get("Records", [])
    if not records:
        logger.warning("Nenhum registro encontrado no evento.")
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
