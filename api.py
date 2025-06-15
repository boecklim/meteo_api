import requests
from flask import Flask, abort

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)


# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def hello_world():
    return 'Hello World'


@app.route('/aemet/start_time/<start_time>/end_time/<end_time>/station/<station>')
# ‘/’ URL is bound with hello_world() function.
def aemet(start_time: str, end_time: str, station: str):
    # only allow “Meteo Station Gabriel de Castilla” => 89070 and “Meteo Station Juan Carlos I” => 89064.

    if station != "89070" and station != "89064":
        abort(400, 'only stations allowed are Meteo Station Gabriel de Castilla (89070) and Meteo Station Juan Carlos I (89064)')

    key = 'eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJtZ2IxQHBvc3Rlby5jaCIsImp0aSI6ImViMTM2MmI2LTRjOGMtNDIxNy1hZGE2LTBiNDE5MjYyZGQyZSIsImlzcyI6IkFFTUVUIiwiaWF0IjoxNzQ5ODg4ODA2LCJ1c2VySWQiOiJlYjEzNjJiNi00YzhjLTQyMTctYWRhNi0wYjQxOTI2MmRkMmUiLCJyb2xlIjoiIn0.jY9v2XDKE7mOZeWppIvzw2Tx4ETdxyRikBj3uZctLag'

    url = f"https://opendata.aemet.es/opendata/api/antartida/datos/fechaini/{start_time}/fechafin/{end_time}/estacion/89064"

    payload = {}
    headers = {
        'Accept': 'application/json',
        'api_key': key,
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return response.text
# 
#
# @app.route('/users/<user_id>/orders/<order_id>', methods=['GET'])
# def get_order(user_id, order_id):
#     return {
#         "user_id": user_id,
#         "order_id": order_id
#     }
#

# main driver function
if __name__ == '__main__':
    # run() method of Flask class runs the application
    # on the local development server.
    app.run(debug=True)
