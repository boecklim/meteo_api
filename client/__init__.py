import requests
import os
from flask import Flask, abort, request

def get_aemet_data(start_time: str, end_time: str, station: str) -> dict:
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
    return resp_data_json
