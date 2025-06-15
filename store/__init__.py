import sqlite3
import logging
import pandas as pd
from datetime import datetime

def get_meteo_data(start_time: datetime, end_time: datetime, station: str) -> pd.DataFrame:
    conn = sqlite3.connect('meteo_data.db')

    try:
        df = pd.read_sql_query(f"select * from meteo_data where date > '{start_time}' and date < '{end_time}' and station = {station}", con=conn)
    except pd.errors.DatabaseError:
        logging.error("database doesn't exist")
        return pd.DataFrame()

    df.reset_index()
    return df.drop(columns=['station'])


def store_meteo_data(df: pd.DataFrame, station: str):
    conn = sqlite3.connect('meteo_data.db')
    df['station'] = station

    df.set_index(['station', 'fhora']).to_sql(name='meteo_data', if_exists='append', index=True, con=conn)
