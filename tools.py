import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime,time, timedelta, date
import csv
import matplotlib
import matplotlib.pyplot as plt
font = {'family' : 'sans',
		'weight' : 'bold',
		'size'   : 22}

matplotlib.rc('font', **font)

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


def compare_stocks(tickers_dic, fixed_ticker, moving_ticker, moving_shift, compare_range, today_date, forecast_trade_days):
	# convert today_date string into datetime object
	today_date = datetime.strptime(today_date, '%Y-%m-%d')
	# read df files from tickers_dic
	df_fix = pd.read_csv(tickers_dic[fixed_ticker]['file_path'],thousands=',', header=0, sep=',', index_col=None,)
	df_mov = pd.read_csv(tickers_dic[moving_ticker]['file_path'],thousands=',', header=0, sep=',', index_col=None,)
	
	# convert Date column to datetime 
	df_fix['Date'] = pd.to_datetime(df_fix['Date'])
	df_mov['Date'] = pd.to_datetime(df_mov['Date'])
	# call the z_score function to normilize the 'Adj. Close' column
	df_fix_nrm, fix_z_params = z_score(df_fix, ['Adj. Close'])
	df_mov_nrm, mov_z_params = z_score(df_mov, ['Adj. Close'])
	print(len(df_fix_nrm), len(df_mov_nrm))
	today_index = np.argmin(abs(df_fix_nrm['Date']-today_date))
	# near_todays_date = df_fix['Date'][today_index]
	# print(near_todays_date, today_date)
	# print (df_mov_nrm['Adj. Close'])	
	# ax1 = plt.subplot(211)
	# ax1.hist(df_mov_nrm['Adj. Close'],bins=100)
	# ax1.hist(df_mov['Adj. Close'],bins=100)
	# ax1 = plt.subplot(212)
	# ax1.plot(df_mov['Date'], df_mov['Adj. Close'])
	# plt.show()
	cropped_df_fix = df_fix_nrm['Adj. Close'][today_index-compare_range:today_index+1]
	cropped_df_mov = df_mov_nrm['Adj. Close'][today_index-compare_range-moving_shift:today_index-moving_shift+1]

	ax1 = plt.subplot(211)
	# ax1.hist(df_mov_nrm['Adj. Close'],bins=100)
	ax1.plot(cropped_df_fix)
	ax1 = plt.subplot(212)
	ax1.plot(cropped_df_mov)
	plt.show()