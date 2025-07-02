from datetime import datetime

import pytz
from configs.env_vars import API_URL, S3_BUCKET
from data.states_mapping import states_coordinates
from loguru import logger
from services.api import ApiService
from services.s3 import S3Service


def run_job(
    state: str,
    values: dict,
    api_service: ApiService,
    s3_service: S3Service,
    extraction_datetime: datetime,
):
    logger.info(f"Processing: {state} - {values['city']}")
    params = {
        "latitude": values["lat"],
        "longitude": values["lon"],
        "hourly": "temperature_2m",
        "timezone": "America/Sao_Paulo",
        "forecast_days": 1,
    }

    try:
        response = api_service.get_response(params)
        if not response:
            logger.error(f"No response for {state} - {values['city']}")
            return
        response["state"] = state
        response["city"] = values["city"]
        response["extraction_datetime"] = extraction_datetime.strftime(
            "%Y-%m-%dT%H:%M:%S"
        )

        file_path = f"{state}/{extraction_datetime.strftime('%Y-%m-%d_%H%M')}.json"
        s3_service.put_object(data=response, key=file_path)
        logger.info(f"Uploaded data for {state} to S3: {file_path}")
    except Exception as e:
        logger.error(f"Failed processing {state}: {e}")


def lambda_handler(event, context):
    extraction_datetime = datetime.now(pytz.timezone("America/Sao_Paulo"))
    api_service = ApiService(API_URL)
    s3_service = S3Service(S3_BUCKET)
    for state, values in states_coordinates.items():
        run_job(state, values, api_service, s3_service, extraction_datetime)


if __name__ == "__main__":
    lambda_handler(None, None)
