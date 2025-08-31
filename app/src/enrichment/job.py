from etl import extract, load, transform
from loguru import logger

from src.common.configs.env_vars import S3_BUCKET


def run_job(body_record):
    # Extract
    try:
        bucket = body_record["s3"]["bucket"]["name"]
        path = body_record["s3"]["object"]["key"]
    except KeyError as e:
        logger.error(f"Key error in body_record: {e}. Record: {body_record}")
        return

    logger.info(f"Processing file: s3://{bucket}/{path}")
    try:
        df = extract.pl_read_parquet_from_s3(bucket, path)
    except Exception as e:
        logger.error(f"Error extracting file {path} from bucket {bucket}: {e}")
        return

    # Transform
    try:
        logger.info("Transforming dataframes")
        descriptions = []
        for row in df.iter_rows(named=True):
            try:
                desc = transform.generate_description(
                    temp=row["temperature_2m"],
                    wind=row["windspeed_10m"],
                    hum=row["relative_humidity_2m"],
                )
                descriptions.append(desc)
            except Exception as e:
                raise (f"Error generating description for row {row}: {e}")

        # Adiciona as descrições geradas ao DataFrame
        df = transform.pl_with_columns(
            df, descriptions, columna_name="weather_description"
        )

        # Create partition columns
        df = transform.pl_create_partition(df, path)
    except Exception as e:
        logger.error(f"Error during transformation: {e}")
        return

    # Load
    try:
        logger.info("Loading dataframes to S3")
        df = df.to_pandas()
        load.write_s3(
            df=df,
            bucket=f"{S3_BUCKET}-enriched",
            key="df_weather_hourly",
            partition_cols=["state", "year", "month", "day", "hour"],
        )
    except Exception as e:
        logger.error(f"Error loading data to S3: {e}")
        return
