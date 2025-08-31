import unicodedata
from datetime import datetime

from loguru import logger

from src.common.configs.env_vars import API_URL, S3_BUCKET
from src.common.services.api import ApiService
from src.common.services.s3 import S3Service


def run_job(
    state: str,
    values: dict,
    extraction_datetime: datetime,
):
    logger.info(f"Processing: {state} - {values['city']}")
    params = {
        "latitude": values["lat"],
        "longitude": values["lon"],
        "hourly": "temperature_2m,relative_humidity_2m,windspeed_10m,precipitation",
        "timezone": "America/Sao_Paulo",
        "forecast_days": 1,
    }

    try:
        response = ApiService(API_URL).get(params)
        if not response:
            logger.warning(f"No response for {state} - {values['city']}")

        response["extraction_datetime"] = extraction_datetime

        city = unicodedata.normalize("NFKD", values["city"].replace(" ", "_").lower())
        city = "".join(c for c in city if unicodedata.category(c) != "Mn")

        file_path = f"{extraction_datetime.replace(':', '-')}/{state}_{city}.json"
        S3Service(f"{S3_BUCKET}-raw", file_path).put_object(data=response)
        logger.info(f"Uploaded data for {state} to S3: {file_path}")
    except Exception as e:
        logger.error(f"Failed processing {state}: {e}")
