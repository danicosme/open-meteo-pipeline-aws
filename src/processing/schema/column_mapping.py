import polars as pl


class ColumnMapping:
    @staticmethod
    def get_weather_columns():
        """
        Returns the column mapping for the weather data.
        """
        return {
            "latitude": pl.Float64,
            "longitude": pl.Float64,
            "generationtime_ms": pl.Float64,
            "utc_offset_seconds": pl.Int64,
            "timezone": pl.String,
            "timezone_abbreviation": pl.String,
            "elevation": pl.Float64,
            "state": pl.String,
            "city": pl.String,
            "extraction_datetime": pl.Datetime(),
        }

    @staticmethod
    def get_weather_columns_hourly():
        """
        Returns the column mapping for the hourly weather data.
        """
        return {
            "time": pl.Datetime(),
            "temperature_2m": pl.Float64,
        }

    @staticmethod
    def get_weather_columns_hourly_units():
        """
        Returns the column mapping for the hourly weather units data.
        """
        return {
            "time": pl.String,
            "temperature_2m": pl.String,
        }