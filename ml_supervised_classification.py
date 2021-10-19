import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime,time, timedelta, date
import matplotlib
import matplotlib.pyplot as plt
from tools import *

font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)
database_path = './data/TSX/20190222'
tickers_dic = get_tickers_dic(database_path)
fixed_ticker = 'AC.TO'
probe_ticker = 'ACB.TO'
index_ticker = 'index_GSPTSE'

shift_val = 60 # trade days difference between fix and moving
interval_val = 215 # duration o the comparision
today_date = '2019-02-01' # start of prediction
forecast_trade_days = 15 # trade days in after today

# index_df = crop_interval(tickers_dic, index_ticker, 0, interval_val, today_date)
# probe_df = crop_interval(tickers_dic, probe_ticker, shift_val, interval_val, today_date)
df = crop_interval(tickers_dic, fixed_ticker, 0, interval_val, today_date)
get_gain_label(df, forecast_trade_days)
# beta_coef = calculate_beta(fixed_df, index_df)
# fixed_df = add_moving_average(fixed_df, [15, 50, 200])

# title = fixed_ticker
# legends = ['Adj. Close','SMA_15','EMA_15', 'SMA_50', 'EMA50']
# plot_stocks(fixed_df['Date'], [fixed_df['Adj. Close'], fixed_df['SMA_15'], fixed_df['EMA_15'],
#         fixed_df['SMA_50'], fixed_df['EMA_50']],
#         legends=legends, title=title)
