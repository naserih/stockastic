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


database_path = r"C:\Users\Robbie\Dropbox\stockastic\data\TSX\20190222"
# read tickers and files.
def get_tickers_dic(database_path):
	tickers_dic = {}
	tickers = [f[:-4] for f in os.listdir(database_path) if ".csv" in f]
	for ticker in tickers:
		tickers_dic[ticker] = {'file_path':os.path.join(database_path,ticker)+'.csv',
									'ticker':ticker}
	return tickers_dic


tickers_dic = get_tickers_dic(database_path)


def add_mean_median_volume(tickers_dic):
	# print (tickers_dic)
	for ticker  in tickers_dic:
		full_file_path = os.path.join(database_path,ticker)+'.csv'
		df = pd.read_csv(full_file_path,thousands=',', header=0, sep=',', index_col=None,)
		tickers_dic[ticker]['df'] = df
		if len(df['Volume']) == 0:
			tickers_dic[ticker]['mean_volume'] = 0
			tickers_dic[ticker]['median_volume'] = 0
		else:
			tickers_dic[ticker]['mean_volume'] = df['Volume'].mean()
			tickers_dic[ticker]['median_volume'] = df['Volume'].median()
		# print(tickers_dic[ticker]['median_volume'])

	return tickers_dic

tickers_dic = add_mean_median_volume(tickers_dic)

def add_tick_order(tickers_dic):
	sorted_mean_by_volume = sorted(tickers_dic, key=lambda k: tickers_dic[k]['mean_volume'], reverse=True)
	# check to make sure it is working 
	for i in range(len(sorted_mean_by_volume)):
		# print(sorted_mean_by_volume[i], tickers_dic[sorted_mean_by_volume[i]]['mean_volume'])
		ticker = sorted_mean_by_volume[i]
		order_mean_volume = i
		tickers_dic[ticker]['order_mean_volume'] = order_mean_volume

	sorted_median_by_volume = sorted(tickers_dic, key=lambda k: tickers_dic[k]['median_volume'], reverse=True)
	for i in range(len(sorted_median_by_volume)):
		ticker = sorted_median_by_volume[i]
		order_median_volume = i
		# print(i, ' < ',ticker, ' > ', tickers_dic[ticker]['median_volume'])
		tickers_dic[ticker]['order_median_volume'] = order_median_volume

tickers_dic = add_tick_order(tickers_dic)

# print(tickers_dic)
# df = pd.DataFrame(tickers_dic.values())
# # print(df.keys())
# ax=df.plot.scatter(x='order_median_volume', 
# 	y='median_volume', 
# 	c='blue'
# 	)
# df.plot.scatter(x='order_median_volume', 
# 	y='mean_volume', 
# 	c='red', ax=ax
# 	)
# plt.legend(['median_volume', 'mean_volume'])
# plt.show()

# def get_sotck_values(ticker, header):
# 	full_file_path = tickers_dic[ticker]['file_path']
# 	df = pd.read_csv(full_file_path,thousands=',', header=0, sep=',', index_col=None)
# 	value_array = df[header]
# 	return value_array
 

# value = get_sotck_values('AC.TO', 'Adj. Close')
# index = 'Adj. Close'
# df = tickers_dic['AC.TO']['df']
# print(df.keys())
# df['Date'] = pd.to_datetime(df['Date'])
# filtered_df = df[(df['Date']>datetime(2016,1,1)) & (df['Date']<datetime(2016,3,1))]
# plt.plot(filtered_df['Date'], filtered_df[index])
# plt.show()

def plot_open_close_ratio(tickers_dic, ticker):
	# read dataframe for a given ticker
	df = tickers_dic[ticker]['df']
	# calculates the ratio of close to open
	close_open_ratio = df['Adj. Close'] / df['Open'] 
	# adds a new colomn as C/O
	df['C/O'] = close_open_ratio
	# calculates the ratio of open to close of the previous day
	open_close_ratio =   df['Open'] / df['Adj. Close'].shift(1)
	open_open_ratio =   df['Open'] / df['Open'].shift(1)

	# adds a new colomn as O/C
	df['O/C'] = open_close_ratio
	df['O/O'] = open_open_ratio
	#
	df.plot.scatter(x='C/O', y='O/C',c='blue' , title=ticker)
	df.plot.scatter(x='C/O', y='O/O',c='red' , title=ticker)

	# plt.show()
	plt.savefig(ticker+'.png')


def plot_volume_close(tickers_dic, ticker):
	# read dataframe for a given ticker
	df = tickers_dic[ticker]['df']
	shift = 30
	pre_volume = df['Volume'].shift(shift)
	df['Pre. Volume'] = pre_volume
	plt.rcParams["figure.figsize"] = [18, 10]
	df.plot.scatter(x='Pre. Volume', y='Adj. Close',c='blue' , title=ticker+' '+str(shift))
	# plt.show()
	plt.savefig('plots/'+ticker+'_'+str(shift)+'.png')
# ticker = 'AC.TO'

# SCAN_RANGE = 10
# for ticker in sorted_median_by_volume[:SCAN_RANGE]:
# 	print (ticker)
	# plot_open_close_ratio(tickers_dic, ticker)
	# plot_volume_close(tickers_dic, ticker)

#Lesson 4: Compare two stock values

def z_score(df, columns):
	''' 
	function to use z-score to normilize the pd column values
	z-score normilized array has mean of zero and standard deviation of 1.
	'''
	z_params = {}
	# copy the dataframe
	df_nrm = df.copy()
	for column in columns:
		df_mean =  df_nrm[column].mean()
		df_std = df_nrm[column].std()
		# store mean and std values
		z_params[column] = {'mean' : df_mean,
					'std': df_std}
		# apply the z-score method
		df_nrm[column] = (df_nrm[column] - df_mean) / df_std
	return df_nrm, z_params

def rev_z_score(df_nrm, z_params):
	'''
	 function to reverse the z-score normilized values to the original
	z_params include std and mean values of original pd columns
	'''
	df = df_nrm.copy()
	columns = z_params.keys()
	for column in columns:
		df[column] = df[column]*z_params[column]['std'] + z_params[column]['mean']
	return df
	 
def compare_stocks(tickers_dic, fixed_ticker, moving_ticker, interval, time_shift, today_date, forecast_days):
	# convert today_date string into datetime object
	today_date = datetime.strptime(today_date, '%Y-%m-%d')
	# read df files from tickers_dic
	df_fix = tickers_dic[fixed_ticker]['df']
	df_mov = tickers_dic[moving_ticker]['df']
	# convert Date column to datetime 
	df_fix['Date'] = pd.to_datetime(df_fix['Date'])
	df_mov['Date'] = pd.to_datetime(df_mov['Date'])
	# call the z_score function to normilize the 'Adj. Close' column
	df_fix_nrm, fix_z_params = z_score(df_fix, ['Adj. Close'])
	df_mov_nrm, mov_z_params = z_score(df_mov, ['Adj. Close'])



 
	# filtered_df = df[(df['Date']>datetime(2016,1,1)) & (df['Date']<datetime(2016,3,1))]


today_date = '2019-01-12'
