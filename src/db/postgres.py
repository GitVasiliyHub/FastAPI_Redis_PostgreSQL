from sqlalchemy import create_engine
import pandas as pd

from config import DATABASE_URL

engine = create_engine(DATABASE_URL)


def download_data(sql: str, **kwargs) -> pd.DataFrame:
    return pd.read_sql(sql=sql, con=engine.connect(), **kwargs)