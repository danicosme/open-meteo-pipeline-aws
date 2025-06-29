import polars as pl


def pl_unnest(df: pl.DataFrame, columns: list, unnest_column: str) -> pl.DataFrame:
    return df.select(pl.col(columns)).unnest(unnest_column)


def pl_unnest_explode(
    df: pl.DataFrame, columns: list, unnest_column: str, explode_columns: list
) -> pl.DataFrame:
    return df.select(columns).unnest(unnest_column).explode(explode_columns)


def pl_cast(df: pl.DataFrame, columns: dict) -> pl.DataFrame:

    for column, dtype in columns.items():
        if "Datetime" in str(dtype):
            df = df.with_columns(pl.col(column).str.to_datetime())

        df = df.with_columns(pl.col(column).cast(dtype))

    return df


def pl_drop_columns(df: pl.DataFrame, columns: list) -> pl.DataFrame:
    df = df.drop(columns)
    return df

def pl_create_partition(df: pl.DataFrame, time_col) -> pl.DataFrame:
    df = df.with_columns(
        pl.col(time_col).dt.year().alias("year"),
        pl.col(time_col).dt.month().alias("month"),
        pl.col(time_col).dt.day().alias("day"),
        pl.col(time_col).dt.hour().alias("hour"),
    )
    return df