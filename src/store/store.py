import sqlite3
import pandas as pd
from datetime import datetime

def get_meteo_data(start_time: datetime, end_time: datetime, station: str) -> pd.DataFrame:
    conn = sqlite3.connect('meteo_data.db')
    query = f"""
    select * from meteo_data 
    where date > '{start_time.strftime("%Y-%m-%d %H:%M:%S")}' 
    and date < '{end_time.strftime("%Y-%m-%d %H:%M:%S")}' 
    and station = {station}
    """
    try:
        df = pd.read_sql_query(query, con=conn)
    except pd.errors.DatabaseError:
        return pd.DataFrame()

    df['date'] = pd.to_datetime(df['date'], format='ISO8601')

    df.drop(columns=['station'], inplace=True)
    return df


def store_meteo_data(df: pd.DataFrame, station: str):
    conn = sqlite3.connect('meteo_data.db')

    df_new = pd.DataFrame(df)
    df_new['station'] = station

    df_new.set_index(['station', 'date']).to_sql(name='meteo_data', if_exists='append', index=True, con=conn)
