import json
from loguru import logger
from run_job import run_job

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
        "Records": [{
            "body": {
                "s3": {
                    "bucket": {"name": "open-meteo-pipeline-aws-processed"},
                    "object": {"key": "df_weather_hourly/state=SP/year=2025/month=7/day=6/hour=0/42084233d8e6496dbde4e36e3d0ce3ef.snappy.parquet"}
                }
            }
        }]
    }
    lambda_handler(event, None)