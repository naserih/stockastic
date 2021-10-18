from tools import read_sorted_files_csv, get_tickers_dic, compare_stocks

database_path = r"C:\Users\Robbie\Dropbox\stockastic\data\TSX\20190222"
sorted_by_median_path = r"C:\Users\Robbie\Dropbox\stockastic\data\sorted_tickers_median_volume.csv"
sorted_by_mean_path = r"C:\Users\Robbie\Dropbox\stockastic\data\sorted_tickers_mean_volume.csv"

tickers_sorted = read_sorted_files_csv(sorted_by_median_path)
tickers_dic = get_tickers_dic(database_path)

fixed_ticker = 'AC.TO'
moving_ticker = 'ACB.TO'
moving_shift = 60 # trade days difference between fix and moving
compare_range = 160 # duration o the comparision
today_date = '2019-01-01' # start of prediction
forecast_trade_days = 20 # trade days in after today
compare_stocks(tickers_dic, fixed_ticker, moving_ticker, moving_shift, compare_range, today_date, forecast_trade_days)	