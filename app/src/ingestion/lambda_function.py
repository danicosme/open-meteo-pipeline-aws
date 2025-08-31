from datetime import datetime
from zoneinfo import ZoneInfo

from data.states_mapping import states_coordinates
from job import run_job

tz = ZoneInfo("America/Sao_Paulo")


def lambda_handler(event, context):
    extraction_datetime = datetime.now(tz).strftime("%Y-%m-%dT%H:%M:%S")
    for state, values in states_coordinates.items():
        run_job(state, values, extraction_datetime)


if __name__ == "__main__":
    lambda_handler(None, None)
