# test_weather.py
import unittest
from unittest.mock import patch, Mock

import pandas as pd

from client import get_aemet_data
from api import get_aemet
from dateutil import parser

class TestGetMeteoData(unittest.TestCase):

    # @patch('store.get_meteo_data')
    def test_get_aemet(self):
        with patch('store.get_meteo_data') as mock_store_get_meteo_data:

            mock_response = Mock()

            mock_response.return_value = pd.read_pickle("test_dataframe")

            mock_response.raise_for_status.return_value = pd.read_pickle("test_dataframe")

            mock_store_get_meteo_data.return_value = mock_response

            start_time = '2025-02-22T00:00:00UTC'
            end_time = '2025-02-23T00:00:00UTC'
            station = '89070'
            result = get_aemet(start_time, end_time, station, ['temp', 'pres', 'vel'], 'hourly')

            start = parser.parse(start_time)
            end = parser.parse(end_time)


            mock_store_get_meteo_data.assert_called_once_with(start, end, station)
            # self.assertEqual(result, expected_data)

if __name__ == '__main__':
    unittest.main()