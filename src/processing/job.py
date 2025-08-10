from etl import extract, load, transform
from loguru import logger
from schema.column_mapping import ColumnMapping

from src.common.configs.env_vars import S3_BUCKET


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
        # Unnest and explode columns to create new dataframes
        df_weather_hourly = transform.pl_unnest_explode(
            df=df_weather,
            columns=["latitude", "longitude", "hourly", "extraction_datetime"],
            unnest_column="hourly",
            explode_columns=[
                "time",
                "temperature_2m",
                "relative_humidity_2m",
                "windspeed_10m",
                "precipitation",
            ],
        )
        df_weather_hourly_units = transform.pl_unnest(
            df=df_weather,
            columns=[
                "hourly_units",
                "extraction_datetime",
            ],
            unnest_column="hourly_units",
        )

        # Drop unnecessary columns
        df_weather = transform.pl_drop_columns(df_weather, ["hourly", "hourly_units"])

        # Enrich dataframes with state and city information
        path_parts = path.split("/")[-1].replace(".json", "")
        state = path_parts.split("_")[0]
        city = " ".join(path_parts.split("_")[1:])

        df_weather = transform.pl_with_columns(
            df=df_weather,
            columns={
                "state": state,
                "city": city,
            },
        )

        df_weather_hourly = transform.pl_with_columns(
            df=df_weather_hourly,
            columns={
                "state": state,
                "city": city,
            },
        )

        # Cast columns
        df_weather = transform.pl_cast(df_weather, ColumnMapping.get_weather_columns())
        df_weather_hourly = transform.pl_cast(
            df_weather_hourly, ColumnMapping.get_weather_columns_hourly()
        )
        df_weather_hourly_units = transform.pl_cast(
            df_weather_hourly_units, ColumnMapping.get_weather_columns_hourly_units()
        )

        # Create partitions
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
            partition_cols=["year", "month", "day", "hour"],
        )
        load.write_s3(
            df=df_weather_hourly_units,
            bucket=f"{S3_BUCKET}-processed",
            key="df_weather_hourly_units",
        )
        logger.info(f"Arquivo {path} processado e salvo com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao salvar dados processados do arquivo {path}: {e}")
