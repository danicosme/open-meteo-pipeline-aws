import re

import polars as pl

from src.common.configs.env_vars import API_ROUTER_URL, MODEL, OPENROUTER_API_KEY
from src.common.services.api import ApiService


def prompt(temp, hum, wind):
    return f"""Temperatura: {temp}°C, Umidade: {hum}%, Vento: {wind} km/h

    Responda APENAS com uma frase simples descrevendo o clima. Não inclua explicações, formatação ou asteriscos. Exemplo: "Dia quente e seco com vento moderado."

    Sua resposta:"""


def generate_description(temp, wind, hum):
    prompt_text = prompt(temp, hum, wind)

    api_service = ApiService(
        url=API_ROUTER_URL,
    )

    result = api_service.post(
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt_text}],
            "temperature": 0,
        },
    )
    return result["choices"][0]["message"]["content"].strip()


def pl_with_columns(df, descriptions, columna_name):
    return df.with_columns([pl.Series(name=columna_name, values=descriptions)])


def pl_create_partition(df: pl.DataFrame, s3_path) -> pl.DataFrame:
    partition_info = _extract_partition_info(s3_path)
    if not partition_info:
        raise ValueError(f"Invalid S3 path: {s3_path}")

    df = df.with_columns(
        pl.lit(partition_info["year"]).alias("year"),
        pl.lit(partition_info["month"]).alias("month"),
        pl.lit(partition_info["day"]).alias("day"),
        pl.lit(partition_info["hour"]).alias("hour"),
    )
    return df


def _extract_partition_info(s3_path):
    pattern = (
        r"df_weather_hourly/year=(\d{4})/month=(\d{1,2})/day=(\d{1,2})/hour=(\d{1,2})"
    )
    match = re.search(pattern, s3_path)

    if match:
        return {
            "year": int(match.group(1)),
            "month": int(match.group(2)),
            "day": int(match.group(3)),
            "hour": int(match.group(4)),
        }
