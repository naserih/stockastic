# from tools import read_sorted_files_csv, add_moving_average, get_tickers_dic, compare_stocks, plot_index, crop_interval, read_csv_as_df, calculate_beta
from tools import *

database_path = r"C:\Users\Robbie\Dropbox\stockastic\data\TSX\20190222"
sorted_by_median_path = r"C:\Users\Robbie\Dropbox\stockastic\data\sorted_tickers_median_volume.csv"
sorted_by_mean_path = r"C:\Users\Robbie\Dropbox\stockastic\data\sorted_tickers_mean_volume.csv"
index_ticker = 'index_GSPTSE'

tickers_sorted = read_sorted_files_csv(sorted_by_median_path)
tickers_dic = get_tickers_dic(database_path)

fixed_ticker = 'AC.TO'
probe_ticker = 'ACB.TO'
# print(tickers_dic[index_ticker])
shift_val = 60 # trade days difference between fix and moving
interval_val = 160 # duration o the comparision
today_date = '2019-01-01' # start of prediction
forecast_trade_days = 20 # trade days in after today
# compare_stocks(tickers_dic, fixed_ticker, moving_ticker, moving_shift, compare_range, today_date, forecast_trade_days)	
# gsptse = read_csv_as_df(tickers_dic[index_ticker]['file_path'])
# print (gsptse['Adj. Close'])

fixed_df = crop_interval(tickers_dic, fixed_ticker, shift_val, interval_val, today_date)
index_df = crop_interval(tickers_dic, index_ticker, shift_val, interval_val, today_date)
probe_df = crop_interval(tickers_dic, probe_ticker, shift_val, interval_val, today_date)
# print(fixed_df['Date'])
# print(index_df['Date'])
beta_coef = calculate_beta(fixed_df, index_df)

print(beta_coef)
# print(covariance)
# print(variance)

# 
fixed_df = add_moving_average(fixed_df, [15, 50, 200])
# print (fixed_df.columns)
title = fixed_ticker
legends = ['Adj. Close','SMA_15','EMA_15', 'SMA_50', 'EMA50']
plot_stocks(fixed_df['Date'], [fixed_df['Adj. Close'], fixed_df['SMA_15'], fixed_df['EMA_15'],
	fixed_df['SMA_50'], fixed_df['EMA_50']],
	legends=legends, title=title)

'''
TODO: lesson 4
- get TSX index [DONE: data/index_GSPTSE.csv]
- read GSPTSE index as df
- compare index_GSPTSE to the fixed ticker
- calculate beta value: covariance(TICKER,GSPTSE)/variance(GSPTSE)
- calculate simple moving average (SMA)
- compare 50-200 day SMA
- compare 15-50 days SMA [DONE]
- calculate exponential moving average (EMA) [DONE!]
'''
