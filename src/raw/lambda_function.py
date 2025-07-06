from datetime import datetime

import pytz
from configs.env_vars import API_URL, S3_BUCKET
from data.states_mapping import states_coordinates
from services.api import ApiService
from services.s3 import S3Service

from run_job import run_job


def lambda_handler(event, context):
    extraction_datetime = datetime.now(pytz.timezone("America/Sao_Paulo")).strftime(
            "%Y-%m-%dT%H:%M:%S"
        )
    api_service = ApiService(API_URL)
    s3_service = S3Service(S3_BUCKET)
    for state, values in states_coordinates.items():
        run_job(state, values, api_service, s3_service, extraction_datetime)


if __name__ == "__main__":
    lambda_handler(None, None)
