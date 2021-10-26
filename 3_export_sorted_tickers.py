#export_sorted_tickers
from tools import get_tickers_dic, sort_by_median_volume, sort_by_mean_volume, write_sorted_files_csv
from tools import add_mean_median_volume
database_path = r"C:\Users\Robbie\Dropbox\stockastic\data\TSX\20190222"
sorted_by_median_path = r"C:\Users\Robbie\Dropbox\stockastic\data\sorted_tickers_median_volume.csv"
sorted_by_mean_path = r"C:\Users\Robbie\Dropbox\stockastic\data\sorted_tickers_mean_volume.csv"

tickers_dic = get_tickers_dic(database_path)
tickers_dic = add_mean_median_volume(tickers_dic)
sorted_median = sort_by_median_volume(tickers_dic)
sorted_mean = sort_by_mean_volume(tickers_dic)
write_sorted_files_csv(sorted_median, tickers_dic, sorted_by_median_path)
write_sorted_files_csv(sorted_mean, tickers_dic, sorted_by_mean_path)

# print (tickers_dic)