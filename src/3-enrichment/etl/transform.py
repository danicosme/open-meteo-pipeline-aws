import polars as pl
from services.api import APIService
from configs.env_vars import OPENROUTER_API_KEY, MODEL, API_URL

def prompt(temp, hum, wind):
    return f"""
    Dado os seguintes dados meteorológicos:
    - Temperatura: {temp}°C
    - Umidade: {hum}%
    - Velocidade do vento: {wind} km/h

    Gere uma frase curta e interpretativa descrevendo o clima do dia.
    Sem repetir os valores numéricos.
    """

def generate_description(temp, wind, hum):
    prompt_text = prompt(temp, hum, wind)

    api_service = APIService(
        url=API_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt_text}],
            "temperature": 0,
        }
    )

    result = api_service.post()
    return result["choices"][0]["message"]["content"].strip()


def pl_with_columns(df, descriptions, columna_name):
    return df.with_columns([pl.Series(name=columna_name, values=descriptions)])