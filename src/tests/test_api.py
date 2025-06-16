import unittest
from unittest.mock import patch, Mock

import pandas as pd

from src.api.api import get_aemet
from dateutil import parser

class TestGetAemet(unittest.TestCase):
    @patch('src.store.store.get_meteo_data', Mock(return_value=pd.read_pickle("test_dataframe")))
    def test_get_aemet(self):

        start_time = '2025-02-22T00:00:00UTC'
        end_time = '2025-02-23T00:00:00UTC'
        station = '89070'
        result = get_aemet(start_time, end_time, station, ['temp', 'pres', 'vel'], 'hourly')

        start = parser.parse(start_time)
        end = parser.parse(end_time)

