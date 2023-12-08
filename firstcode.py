import sys
import os
import pandas as pd
import numpy as np
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
# print (tickers_dic)
for ticker  in tickers_dic:
	full_file_path = os.path.join(database_path,ticker)+'.csv'
	df = pd.read_csv(full_file_path,thousands=',', header=0, sep=',', index_col=None)
	if len(df['Volume']) == 0:
		tickers_dic[ticker]['mean_volume'] = 0
		tickers_dic[ticker]['median_volume'] = 0
	else:
		tickers_dic[ticker]['mean_volume'] = df['Volume'].mean()
		tickers_dic[ticker]['median_volume'] = df['Volume'].median()
	# print(tickers_dic[ticker]['median_volume'])
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
	print(i, ' < ',ticker, ' > ', tickers_dic[ticker]['median_volume'])
	tickers_dic[ticker]['order_median_volume'] = order_median_volume


# print(tickers_dic)
df = pd.DataFrame(tickers_dic.values())
print(df.keys())
ax=df.plot.scatter(x='order_median_volume', 
	y='median_volume', 
	c='blue'
	)
df.plot.scatter(x='order_median_volume', 
	y='mean_volume', 
	c='red', ax=ax
	)
plt.legend(['median_volume', 'mean_volume'])
plt.show()
 



