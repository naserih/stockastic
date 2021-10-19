import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime,time, timedelta, date
import matplotlib
import matplotlib.pyplot as plt
font = {'family' : 'normal',
        'weight' : 'bold',
        'size'   : 22}

matplotlib.rc('font', **font)

database_path = './data/TSX/20190222'

# read tickers and files.
def get_tickers_dic(database_path):
        tickers_dic = {}
        tickers = [f[:-4] for f in os.listdir(database_path) if ".csv" in f]
        for ticker in tickers:
                tickers_dic[ticker] = {'file_path':os.path.join(database_path,ticker)+'.csv',
                                                                        'ticker':ticker}
        return tickers_dic


tickers_dic = get_tickers_dic(database_path)
# print (tickers_dic)
# for ticker  in tickers_dic:
#         df = pd.read_csv(tickers_dic[ticker]['file_path'],thousands=',', header=0, sep=',', index_col=None,)
#         tickers_dic[ticker]['df'] = df
#         if len(df['Volume']) == 0:
#                 tickers_dic[ticker]['mean_volume'] = 0
#                 tickers_dic[ticker]['median_volume'] = 0
#         else:
#                 tickers_dic[ticker]['mean_volume'] = df['Volume'].mean()
#                 tickers_dic[ticker]['median_volume'] = df['Volume'].median()
#         # print(tickers_dic[ticker]['median_volume'])

# sorted_mean_by_volume = sorted(tickers_dic, key=lambda k: tickers_dic[k]['mean_volume'], reverse=True)
# check to make sure it is working 
# for i in range(len(sorted_mean_by_volume)):
#         # print(sorted_mean_by_volume[i], tickers_dic[sorted_mean_by_volume[i]]['mean_volume'])
#         ticker = sorted_mean_by_volume[i]
#         order_mean_volume = i
#         tickers_dic[ticker]['order_mean_volume'] = order_mean_volume


# sorted_median_by_volume = sorted(tickers_dic, key=lambda k: tickers_dic[k]['median_volume'], reverse=True) 
# for i in range(len(sorted_median_by_volume)):
#         ticker = sorted_median_by_volume[i]
#         order_median_volume = i
#         # print(i, ' < ',ticker, ' > ', tickers_dic[ticker]['median_volume'])
#         tickers_dic[ticker]['order_median_volume'] = order_median_volume

def compare_stocks(tickers_dic, fixed_ticker, moving_ticker, interval, time_shift, today_date, forecast_days):
        print (tickers_dic[ticker])

# print sorted_median_by_volume
fixed_ticker = 'AC.TO'
moving_ticker = 'ACB.TO'
interval = 160
forecast_days = 20
time_shift = 60
today_date = '2019-02-12'



# compare_stocks()
