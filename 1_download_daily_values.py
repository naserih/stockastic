'''
list of tickers for each exchange is dmanually ownloaded
from http://eoddata.com/stocklist/
'''

from tools import *
import env

dataroot = './data'
exchange = 'NYSE'# 'NASDAQ' # 'NYSE' # 'TSX'
exchange_ticker_list_path = '%s/%s.txt'%(dataroot,exchange)
exchange_data_folder = '%s/%s'%(dataroot,exchange)
if not os.path.exists(exchange_data_folder):
	os.makedirs(exchange_data_folder)

start_date = datetime(2000, 1, 1)
last_date  = datetime.now().strftime("%Y%m%d")
date_subfolder = '%s/%s'%(exchange_data_folder,last_date)
if not os.path.exists(date_subfolder):
	os.makedirs(date_subfolder)


ticker_list = read_tickers_list(exchange_ticker_list_path)
ticker = 'AAPL'

cnt = 0
for ticker in ticker_list:
	cnt += 1
	ticker_data_filepath = '%s/%s.csv'%(date_subfolder,ticker)
	if os.path.exists(ticker_data_filepath):
		print ('%i/%i: In downloads: %s'%(cnt,len(ticker_list),ticker))
	else:
		try:
			stock_prices_df = get_daily_prices(ticker, start_date)
			stock_prices_df.to_csv(ticker_data_filepath)
			print ('%i/%i Downloaded: %s'%(cnt,len(ticker_list),ticker))
		except Exception as e:
			print (e)
			print ('%i/%i Failed: %s'%(cnt,len(ticker_list),ticker))




