# 8_get_daily_values_yahoo.py
from tools import *
import env

start_date = datetime(2020, 1, 1)
ticker = 'AC.TO'

import requests
from get_all_tickers import get_tickers as gt

from get_all_tickers.get_tickers import Region
# tickers of all exchanges

from get_all_tickers import get_tickers as gt

list_of_tickers = gt.get_tickers()
# url = 'http://maps.googleapis.com/maps/api/directions/json'


# url = 'https://api.nasdaq.com/api/screener/stocks?tableonly=true&limit=25&offset=0&download=true'
# url = "https://api.github.com"

# url = "http://maps.googleapis.com/maps/api/geocode/json?address=google"

# get_tickers(NYSE=True, NASDAQ=True, AMEX=True)
# # params = dict(
#     origin='Chicago,IL',
#     destination='Los+Angeles,CA',
#     waypoints='Joplin,MO|Oklahoma+City,OK',
#     sensor='false'
# )

# resp = requests.get(url=url)
# data = resp.json()

# dic = stock_list(url)

# print (data)
# df = daily_stock_values(ticker, start_date)
# print (df)