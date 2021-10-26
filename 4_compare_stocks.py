# from tools import read_sorted_files_csv, add_moving_average, get_tickers_dic, compare_stocks, plot_index, crop_interval, read_csv_as_df, calculate_beta
from tools import *
import env

database_path = env.database_path
sorted_by_median_path = env.sorted_by_median_path
sorted_by_mean_path = env.sorted_by_mean_path 

index_ticker = 'index_GSPTSE'

tickers_sorted = read_sorted_files_csv(sorted_by_median_path)
tickers_dic = get_tickers_dic(database_path)

# ticker = 'AC.TO'
ticker = tickers_sorted[20]
# probe_ticker = 'ACB.TO'
# print(tickers_dic[index_ticker])
shift_val = 60 # trade days difference between fix and moving
interval_val = 160 # duration o the comparision
today_date = '2019-01-01' # start of prediction
# forecast_trade_days = 20 # trade days in after today
# compare_stocks(tickers_dic, ticker, moving_ticker, moving_shift, compare_range, today_date, forecast_trade_days)	
# gsptse = read_csv_as_df(tickers_dic[index_ticker]['file_path'])
# print (gsptse['Adj. Close'])


'''
TODO: lesson 5
- get TSX index [DONE: data/index_GSPTSE.csv]
- read GSPTSE index as df
- compare index_GSPTSE to the fixed ticker
- calculate beta value: covariance(TICKER,GSPTSE)/variance(GSPTSE)
- calculate simple moving average (SMA)
- compare 50-200 day SMA
- compare 15-50 days SMA [DONE]
- calculate exponential moving average (EMA) [DONE!]
'''

df = crop_interval(tickers_dic, ticker, shift_val, interval_val, today_date)
# index_df = crop_interval(tickers_dic, index_ticker, shift_val, interval_val, today_date)
# probe_dof = crop_interval(tickers_dic, probe_ticker, shift_val, interval_val, today_date)
# print(df['Date'])
# print(index_df['Date'])
# beta_coef = calculate_beta(df, index_df)

# print(beta_coef)
# print(covariance)
# print(variance)

# 
df = add_moving_average(df, [15, 50, 200])
df = add_atr(df, 14)

print (df)

print ('------')
print (t)
# print (df.columns)
# title = ticker
# legends = ['Adj. Close','EMA_15',  'EMA_50']
# plot_stocks(df['Date'], [df['Adj. Close'], df['EMA_15'], df['EMA_50']],
# 	legends=legends, title=title)


'''
TODO: lesson 6
- write a function to compare stock Close value when EMA15 and EMA50 cross
- get the rasing or falling sign for crossing point (compare EMAs before and after cross)
- calculate gain between crossings (Close rasing - close falling)
- 
'''
ema_short = 'EMA_15'
ema_long = 'EMA_50'
cross_points, cross_df = compare_ema(df, ema_short, ema_long, ticker)
# cross_df['cross_sign']
# print(cross_df)
gain_period,gain_value = calculate_gain(cross_df)
print (ticker, gain_period, gain_value)

plot = plot_stocks([df['Date'],df['Date'],df['Date'], cross_df['cross_date'][cross_df['cross_sign']<0],
	cross_df['cross_date'][cross_df['cross_sign']>0],df[ema_short]], 
			[df['Adj. Close'], df[ema_short],df[ema_long], 
			cross_df['cross_val'][cross_df['cross_sign']<0],cross_df['cross_val'][cross_df['cross_sign']>0]],
				markers=['','','','o', 's'],
				linestyles=['-','--','--', 'None', 'None'],
				legends=['Adj. Close',ema_short,ema_long, 'Buy_point', 'Sell_point'],
				title= '%s_Active Days:%i_Gain: %6.2f%%'%(ticker,gain_period,gain_value)
				)
plt_show(plot)
# plt_save(plot, )
# for i in cross_sign:

