# 8_get_daily_values_yahoo.py
from tools import *
import env

start = dt.datetime(2020, 1, 1)
ticker = 'AC.TO'
df = daily_stock_values(ticker, start_date)

print (df)