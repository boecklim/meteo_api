import requests
import os
import pandas as pd
from flask import Flask, abort, request
from dotenv import load_dotenv
import numpy as np

app = Flask(__name__)

@app.route('/aemet/start_time/<start_time>/end_time/<end_time>/station/<station>')
def aemet(start_time: str, end_time: str, station: str):

    # only allow “Meteo Station Gabriel de Castilla” => 89070 and “Meteo Station Juan Carlos I” => 89064.
    if station != "89070" and station != "89064":
        abort(400, 'only stations allowed are Meteo Station Gabriel de Castilla (89070) and Meteo Station Juan Carlos I (89064)')

    query_params = request.args.to_dict(flat=False)

    types = ['temp', 'pres', 'vel']

    if query_params.get('type') is not None:
        types = query_params.get('type')
        # Todo: ignore all values other than 'temp', 'pres', 'vel

    agg_param = None

    if query_params.get('agg') is not None:
        agg_param = query_params.get('agg')[0]
        # Todo: ensure agg_param has only one value

    key = os.environ['API_KEY']

    url = f"https://opendata.aemet.es/opendata/api/antartida/datos/fechaini/{start_time}/fechafin/{end_time}/estacion/{station}"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'api_key': key,
    }

    resp = requests.request("GET", url, headers=headers, data=payload)

    if resp.status_code != 200:
        abort(resp.status_code, resp.text)

    resp_json = resp.json()

    if resp_json['estado'] != 200:
        abort(resp_json['estado'], resp_json['descripcion'])

    resp_data = requests.request("GET", resp_json['datos'], headers=headers, data=payload)
    if resp_data.status_code != 200:
        abort(resp_data.status_code, resp_data.text)

    resp_data_json = resp_data.json()

    df = pd.DataFrame(resp_data_json)
    df['date'] = pd.to_datetime(df['fhora'], format='ISO8601')
    df = df[types + ['date']]
    df.replace('NaN', np.nan, inplace=True)
    df.dropna(how='any', inplace=True)  # remove rows where values are missing

    df['date_hour'] = df['date'].dt.round('h')
    df['date_day'] = df['date'].dt.round('d')
    df['date_month'] = df['date'].dt.to_period("M").dt.to_timestamp()

    data = df.drop(columns=['date_hour', 'date_day', 'date_month']).to_dict('records')

    location = "Europe/Madrid"

    match agg_param:
        case None:
            return data
        case 'hourly':
            df['date_str'] = df['date_hour'].dt.tz_convert(location).astype(str)
        case 'daily':
            df['date_str'] = df['date_day'].dt.tz_convert(location).astype(str)
        case 'monthly':
            df['date_str'] = df['date_month'].dt.tz_convert(location).astype(str)

    data = df.groupby(by='date_str').mean().drop(columns=['date_day', 'date_month', 'date', 'date_hour']).reset_index().rename(columns={'date_str': 'date'}).to_dict('records')

    return data

# main driver function
if __name__ == '__main__':
    load_dotenv()

    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)
