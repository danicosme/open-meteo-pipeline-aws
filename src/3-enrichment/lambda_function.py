import polars as pl
import requests
import io

from configs.env_vars import OPENROUTER_API_KEY, MODEL

from services.s3 import S3Service

def generate_description(temp, wind, hum):
    prompt = f"""
    Dado os seguintes dados meteorológicos:
    - Temperatura: {temp}°C
    - Umidade: {hum}%
    - Velocidade do vento: {wind} km/h

    Gere uma frase curta e interpretativa descrevendo o clima do dia.
    Sem repetir os valores numéricos.
    """
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
        }
    )
    result = response.json()
    return result["choices"][0]["message"]["content"].strip()

def lambda_handler(event, context):
    bucket = event["Records"][0]["s3"]["bucket"]["name"]
    key = event["Records"][0]["s3"]["object"]["key"]

    response = S3Service(bucket=bucket, key=key).get_object()
    df = pl.read_parquet(io.BytesIO(response))

    descriptions = []
    for row in df.iter_rows(named=True):
        try:
            desc = generate_description(
                temp=row["temperature_2m"],
                wind=row["windspeed_10m"],
                hum=row["relative_humidity_2m"]
            )
            descriptions.append(desc)
        except Exception as e:
            raise(f"Erro ao gerar descrição: {e}")
        

    df = df.with_columns([pl.Series(name="weather_description", values=descriptions)])

    print(df)


if __name__ == "__main__":
    event = {
        "Records": [{
            "s3": {
                "bucket": {"name": "open-meteo-pipeline-aws-processed"},
                "object": {"key": "df_weather_hourly/state=SP/year=2025/month=7/day=6/hour=0/42084233d8e6496dbde4e36e3d0ce3ef.snappy.parquet"}
            }
        }]
    }
    lambda_handler(event, None)