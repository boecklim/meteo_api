from client import get_aemet_data
import pandas as pd
from flask import Flask, abort, request
from dotenv import load_dotenv
import numpy as np
from store import store_meteo_data, get_meteo_data
from dateutil import parser
import logging

app = Flask(__name__)

@app.route('/aemet/start_time/<start_time>/end_time/<end_time>/station/<station>')
def aemet(start_time: str, end_time: str, station: str):
    bad_request = 400
    internal_server_error = 500
    # only allow “Meteo Station Gabriel de Castilla” => 89070 and “Meteo Station Juan Carlos I” => 89064.
    if station != "89070" and station != "89064":
        abort(bad_request, 'only stations allowed are Meteo Station Gabriel de Castilla (89070) and Meteo Station Juan Carlos I (89064)')

    query_params = request.args.to_dict(flat=False)

    types = ['temp', 'pres', 'vel']

    if query_params.get('type') is not None:
        types = query_params.get('type')
        # Todo: ignore all values other than 'temp', 'pres', 'vel'


    aggregation = None

    if query_params.get('agg') is not None:
        agg_param = query_params.get('agg')
        if len(agg_param) > 0:
            aggregation = agg_param[0]

    try:
        start = parser.parse(start_time)
    except Exception:
        abort(bad_request, f"start time cannot be parsed {start_time}")

    try:
        end = parser.parse(end_time)
    except Exception:
        abort(bad_request, f"end time cannot be parsed {end_time}")

    fetched_new_data = False

    # Check if data can be found in store
    app.logger.info("getting data from store")
    df = get_meteo_data(start, end, station)
    if df.size == 0: # Todo: check if data fills the whole time frame, if not get missing data from AEMET api
        app.logger.info("no data found in store - getting data from API")
        try:
            aemet_data = get_aemet_data(start_time, end_time, station)
        except Exception:
            app.logger.error("failed to get data from API")
            abort(internal_server_error, "failed to get data")

        df = pd.DataFrame(aemet_data)
        fetched_new_data = True

        df['date'] = pd.to_datetime(df['fhora'], format='ISO8601')


        df = df[types + ['date']]
        df.replace('NaN', np.nan, inplace=True)

        df.dropna(how='any', inplace=True)  # remove rows where values are missing

        if df.size == 0:
            app.logger.error('no values found')
            return abort(internal_server_error, "no values found")

    if fetched_new_data:
        app.logger.info("storing data")
        store_meteo_data(df, station)

    df['date_hour'] = df['date'].dt.round('h')
    df['date_day'] = df['date'].dt.round('d')
    df['date_month'] = df['date'].dt.to_period("M").dt.to_timestamp()

    location = "Europe/Madrid"

    match aggregation:
        case None:
            df['date_str'] = df['date'].dt.tz_convert(location).astype(str)
            return df.drop(columns=['date_hour', 'date_day', 'date_month', 'date']).rename(columns={'date_str': 'date'}).to_dict('records')
        case 'hourly':
            df['date_str'] = df['date_hour'].dt.tz_convert(location).astype(str)
        case 'daily':
            df['date_str'] = df['date_day'].dt.tz_convert(location).astype(str)
        case 'monthly':
            df['date_str'] = df['date_month'].dt.tz_convert(location).astype(str)
        case _:
            abort(bad_request, f"invalid aggregation value {aggregation} - must be one of 'hourly', 'daily', 'monthly'")


    data = df.groupby(by='date_str').mean().drop(columns=['date_day', 'date_month', 'date', 'date_hour']).reset_index().rename(columns={'date_str': 'date'}).to_dict('records')

    return data

# main driver function
if __name__ == '__main__':
    load_dotenv()
    app.logger.setLevel(logging.INFO)

    app.logger.info('Starting API')

    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)
