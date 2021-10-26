import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime,time, timedelta, date
import csv
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats import linregress
import pandas_datareader as pdr

font = {'family' : 'sans',
		'weight' : 'bold',
		'size'   : 22}

matplotlib.rc('font', **font)


def daily_stock_values(ticker, start_date):
	data = pdr.get_data_yahoo(ticker, start_date)
	return data


def get_tickers_dic(database_path):
	tickers_dic = {}
	tickers = [f[:-4] for f in os.listdir(database_path) if ".csv" in f]
	for ticker in tickers:
		tickers_dic[ticker] = {'file_path':os.path.join(database_path,ticker)+'.csv',
									'ticker':ticker}
	return tickers_dic

def add_mean_median_volume(tickers_dic):
	# print (tickers_dic)
	for ticker  in tickers_dic:
		df = pd.read_csv(tickers_dic[ticker]['file_path'],thousands=',', header=0, sep=',', index_col=None,)
		# tickers_dic[ticker]['df'] = df
		if len(df['Volume']) == 0:
			tickers_dic[ticker]['mean_volume'] = 0
			tickers_dic[ticker]['median_volume'] = 0
		else:
			tickers_dic[ticker]['mean_volume'] = df['Volume'].mean()
			tickers_dic[ticker]['median_volume'] = df['Volume'].median()
		# print(tickers_dic[ticker]['median_volume'])
	return tickers_dic

def sort_by_median_volume(tickers_dic):
	return sorted(tickers_dic, key=lambda k: tickers_dic[k]['median_volume'], reverse=True)

def sort_by_mean_volume(tickers_dic):	
	return sorted(tickers_dic, key=lambda k: tickers_dic[k]['mean_volume'], reverse=True)

def write_sorted_files_csv(sorted_tickers, tickers_dic, output_file_full_path):
	with open (output_file_full_path, 'w', newline='',) as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerow(['ticker', 'mean_volume', 'median_volum'])
		csvwriter.writerows([[f, tickers_dic[f]['mean_volume'], tickers_dic[f]['median_volume']] for f in sorted_tickers])

def read_sorted_files_csv(input_file_full_path):
	with open (input_file_full_path, 'r',) as csvfile:
		csvreader = csv.reader(csvfile)
		header = next(csvreader)
		return [f[0] for f in csvreader]

def write_to_csv(array, output_file_full_path):
	with open (output_file_full_path, 'w', newline='',) as csvfile:
		csvwriter = csv.writer(csvfile)
		csvwriter.writerows(array)

def read_csv_as_df(file_path):
	df = pd.read_csv(file_path,thousands=',', header=0, sep=',', 
		index_col=None,na_values=['null'], )
	df = df.fillna(method='ffill')
	return df
		
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
	df_org = df_nrm.copy()
	columns = z_params.keys()
	for column in columns:
		df_org[column] = df_org[column]*z_params[column]['std'] + z_params[column]['mean']
	return df_org

def crop_interval(tickers_dic, ticker, shift, interval, today_date):
	# convert today_date string into datetime object
	today_date = datetime.strptime(today_date, '%Y-%m-%d')
	# read df files from tickers_dic
	df_orig = read_csv_as_df(tickers_dic[ticker]['file_path'])
	# convert Date column to datetime 
	df_orig['Date'] = pd.to_datetime(df_orig['Date'])
	today_index = np.argmin(abs(df_orig['Date']-today_date))

	df_orig = df_orig.truncate(before=today_index-interval-shift+1, after=today_index-shift)
	# print(len(df_orig))
	return df_orig.reset_index()

def calculate_beta(ticker_df, index_df):
	matrix  = {"ticker":(ticker_df['Adj. Close']-ticker_df['Adj. Close'].shift(1))/ticker_df['Adj. Close'].shift(1),
			   "index":(index_df['Adj. Close']-index_df['Adj. Close'].shift(1))/index_df['Adj. Close'].shift(1)}
	df  = pd.DataFrame(data=matrix)
	df = df.dropna()
	df = df.fillna(method='ffill')
	df = df.reset_index()
	covariance = df.cov()
	variance = df.var()
	beta_coef = covariance/variance
	slope, intercept, r_value, p_value, std_err = linregress(df['index'], df['ticker'])
	# print (slope)
	return slope


def add_atr(df, window=14):
	high_low = df['High'] - df['Low']
	high_close = np.abs(df['High'] - df['Adj. Close'].shift())
	low_close = np.abs(df['Low'] - df['Adj. Close'].shift())
	ranges = pd.concat([high_low, high_close, low_close], axis=1)
	true_range = np.max(ranges, axis=1)
	df['ATR_{}'.format(window)] = true_range.rolling(window).sum()/window
	return df

def add_moving_average(df, windows):
	for window in windows:
		df['SMA_{}'.format(window)] = df['Adj. Close'].rolling(window= window).mean()
		df['EMA_{}'.format(window)] = df['Adj. Close'].ewm(span=window, adjust=False).mean()
		df['TMA_{}'.format(window)] = df['EMA_{}'.format(window)].ewm(span=window, adjust=False).mean()
		df['TMA_{}'.format(window)] = df['TMA_{}'.format(window)].ewm(span=window, adjust=False).mean()
	return df

def get_gain_label(df, forecast_trade_days):
	df_nrm, z_params = z_score(df, ['Adj. Close'])
	X = df_nrm['Adj. Close'][:-forecast_trade_days]
	Y = df_nrm['Adj. Close'][-forecast_trade_days:]


def compare_stocks(tickers_dic, fixed_ticker, moving_ticker, moving_shift, compare_range, today_date, forecast_trade_days):
	# convert today_date string into datetime object
	today_date = datetime.strptime(today_date, '%Y-%m-%d')
	# read df files from tickers_dic
	df_fix = read_csv_as_df(tickers_dic[fixed_ticker]['file_path'])
	df_mov = read_csv_as_df(tickers_dic[moving_ticker]['file_path'])
	# convert Date column to datetime 
	df_fix['Date'] = pd.to_datetime(df_fix['Date'])
	df_mov['Date'] = pd.to_datetime(df_mov['Date'])
	# call the z_score function to normilize the 'Adj. Close' column
	df_fix_nrm, fix_z_params = z_score(df_fix, ['Adj. Close'])
	df_mov_nrm, mov_z_params = z_score(df_mov, ['Adj. Close'])
	print(len(df_fix_nrm), len(df_mov_nrm))
	today_fix_index = np.argmin(abs(df_fix_nrm['Date']-today_date))
	today_mov_index = np.argmin(abs(df_mov_nrm['Date']-today_date))
	near_todays_fix_date = df_fix['Date'][today_fix_index-160]
	near_todays_mov_date = df_mov['Date'][today_mov_index-160]
	
	# print(near_todays_fix_date, near_todays_mov_date)
	# print (df_mov_nrm['Adj. Close'])	
	# ax1 = plt.subplot(211)
	# ax1.hist(df_mov_nrm['Adj. Close'],bins=100)
	# ax1.hist(df_mov['Adj. Close'],bins=100)
	# ax1 = plt.subplot(212)
	# ax1.plot(df_mov['Date'], df_mov['Adj. Close'])
	# plt.show()
	cropped_close_fix = df_fix_nrm['Adj. Close'][today_fix_index-compare_range:today_fix_index+1]
	cropped_close_mov = df_mov_nrm['Adj. Close'][today_mov_index-compare_range-moving_shift:today_mov_index-moving_shift+1]
	cropped_date_fix = df_fix_nrm['Date'][today_fix_index-compare_range:today_fix_index+1]
	cropped_date_mov = df_mov_nrm['Date'][today_mov_index-compare_range-moving_shift:today_mov_index-moving_shift+1]


	ax1 = plt.subplot(211)
	# ax1.hist(df_mov_nrm['Adj. Close'],bins=100)
	ax1.plot(cropped_date_fix, cropped_close_fix)
	ax1 = plt.subplot(212)
	ax1.plot(cropped_date_mov, cropped_close_mov)
	plt.show()

def compare_ema(df, ema_short, ema_long, ticker):	
	ema_diff = df[ema_short]-df[ema_long]
	shifted_ema_diff = ema_diff.shift(-1)
	# print (ema_diff)
	ratio = ema_diff/shifted_ema_diff
	ema_diff[ema_diff>0] = 1 # sell point
	ema_diff[ema_diff<0] = -1 # buy point
	matrix  = {"cross_date":df['Date'][ratio<0],
			   "cross_sign": ema_diff[ratio<0],
			   "cross_val":df['Adj. Close'][ratio<0]}
	dataFrame  = pd.DataFrame(data=matrix)
	# print(df['Date'][ratio<=0])
	# print (ratio<=0)

	return ratio<0, dataFrame.reset_index()


def calculate_gain(cross_df):
	gain_value = 0
	gain_period = 0
	if len(cross_df['cross_val']>2):	
		gain_value = ((cross_df['cross_val']-cross_df['cross_val'].shift(-1))*cross_df['cross_sign']/cross_df['cross_val']*100).sum()
		gain_period = (cross_df['cross_date'][len(cross_df['cross_date'])-1]-cross_df['cross_date'][0]).days
	return gain_period, gain_value

def plot_stocks(ts, ys, legends=[''], title = '', markers=[''], linestyles=['dashed']):
	plt.rcParams["figure.figsize"] = [18, 6]
	for z in zip(ts, ys,markers, linestyles):
		plt.plot(z[0], z[1], marker=z[2], linestyle=z[3])
		plt.legend(legends)
		plt.title(title)
	return plt

def plt_show(plt):
	plt.show()

def plt_save(plt, path):
	plt.savefig(path)
	# plt.close()
	plt.clf()

def plot_index(df_x, df_y):
	# read dataframe for a given ticker
	# for row in df_x['Adj. Close']:
	# 	print (row)
	# print(len(df_x['Adj. Close']),len(df_y['Adj. Close']))
	# print(df_x['Adj. Close']-df_y['Adj. Close'])
	plt.plot(df_x['Adj. Close'], df_y['Adj. Close'])
	# linear_regressor = LinearRegression()  # create object for the class
	# linear_regressor.fit(df_x['Adj. Close'], df_y['Adj. Close'])  # perform linear regression
	print(slope)

	matrix  = {	"x_Date":df_x['Date'],
				"y_Date":df_y['Date'],
				"x":df_x['Adj. Close'],
			   	"y":df_y['Adj. Close']}
	dataFrame  = pd.DataFrame(data=matrix)
	covariance = dataFrame.cov()
	plt.rcParams["figure.figsize"] = [18, 10]
	dataFrame.plot.scatter(x='x', y='y',c='blue' , title="stock vs index")
	ax1 = dataFrame.plot.line(x='x_Date', y='x',c='red' , title="stock vs index")
	dataFrame.plot.line(ax=ax1, x='y_Date', y='y',c='green' , title="stock vs index", secondary_y=True)
	plt.show()
	# plt.savefig('plots/'+df_x+'.png')



