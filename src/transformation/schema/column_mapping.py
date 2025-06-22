import polars as pl

weather_columns = {
    'latitude': pl.Float64, 
    'longitude': pl.Float64,
    'generationtime_ms': pl.Float64,
    'utc_offset_seconds': pl.Int64,
    'timezone': pl.String,
    'timezone_abbreviation': pl.String, 
    'elevation': pl.Float64,
    'state': pl.String, 
    'city': pl.String,
    'extraction_datetime': pl.Datetime(),
}

weather_columns_hourly = {
    'time': pl.Datetime(),
    'temperature_2m': pl.Float64,
}

weather_columns_hourly_units = {
    'time': pl.String,
    'temperature_2m': pl.String,
}