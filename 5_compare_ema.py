# 5_compare_ema.py
from tools import *

database_path = r"C:\Users\Robbie\Dropbox\stockastic\data\TSX\20190222"
sorted_by_median_path = r"C:\Users\Robbie\Dropbox\stockastic\data\sorted_tickers_median_volume.csv"
sorted_by_mean_path = r"C:\Users\Robbie\Dropbox\stockastic\data\sorted_tickers_mean_volume.csv"
index_ticker = 'index_GSPTSE'

tickers_sorted = read_sorted_files_csv(sorted_by_median_path)
tickers_sorted.append(index_ticker)
tickers_dic = get_tickers_dic(database_path)

def run_compare(shift_val, interval_val, moving_averages, directory):
	gains = [['ticker', 'normal_gain','gain_period', 'ema_gain', 'beta_coef']]
	index_df = crop_interval(tickers_dic, index_ticker, shift_val, interval_val, today_date)
	index_df = add_moving_average(index_df, moving_averages)
		
	cross_points, cross_df = compare_ema(index_df, ema_short, ema_long, index_ticker)
	gain_period, gain_value = calculate_gain(cross_df)
	beta_coef = calculate_beta(index_df, index_df)
	normal_gain = (index_df['Adj. Close'][len(index_df)-1]-index_df['Adj. Close'][0])/index_df['Adj. Close'][0]*100
	gains.append([index_ticker, normal_gain, gain_period, gain_value, beta_coef])
	cnt = 0	
	plot_names = ['_'.join(f.split('_')[1:8]) for f in os.listdir('output')]
	# print(plot_names)
	for ticker in tickers_sorted[:300]:
		cnt += 1
		print (ticker) 
		df = crop_interval(tickers_dic, ticker, shift_val, interval_val, today_date)
		if len(df['Date']) > 0:
			df = add_moving_average(df, moving_averages)
			beta_coef = calculate_beta(df, index_df)
			# print('beta_coef', beta_coef)
			# print ('df>>', df)
			normal_gain = (df['Adj. Close'][len(df['Adj. Close'])-1]-df['Adj. Close'][0])/df['Adj. Close'][0]*100
			cross_points, cross_df = compare_ema(df, ema_short, ema_long, ticker)
			gain_period, gain_value = calculate_gain(cross_df)
		else:
			gain_period = 0
			gain_value = 0
			normal_gain = 0
			beta_coef = 0			
		gains.append([ticker, normal_gain, gain_period, gain_value, beta_coef])
		title = '_%s_%i_%i_%s_%s_Active Days%i_Gain %6.2fp'%(ticker,shift_val, interval_val, ema_long,ema_short, gain_period,gain_value)
		try:
			if not os.path.exists(directory+'/'+title+'.png'):
				plot = plot_stocks([df['Date'],df['Date'],df['Date'], cross_df['cross_date'][cross_df['cross_sign']<0],
					cross_df['cross_date'][cross_df['cross_sign']>0],df[ema_short]], 
							[df['Adj. Close'], df[ema_short],df[ema_long], 
							cross_df['cross_val'][cross_df['cross_sign']<0],cross_df['cross_val'][cross_df['cross_sign']>0]],
								markers=['','','','o', 's'],
								linestyles=['-','--','--', 'None', 'None'],
								legends=['Adj. Close',ema_short,ema_long, 'Buy_point', 'Sell_point'],
								title= title
								)
				# plt_show(plot)
				plt_save(plot, directory+'/'+title+'.png')
			# print(cnt, ticker, '%5.0f%%'%gain_value, end="")
			# else:
			# 	print('saved!')
		except:
			print ('plot failed: \t', title)
		if cnt%10 == 0:
			print("|", end="")
	# plot.close('all')
	write_to_csv(gains,directory+'.csv')



today_date = '2019-02-22' # start of prediction
# shift_val = 0 # trade days difference between fix and moving
# interval_val = 160 # duration o the comparision
# moving_averages = [21,200] #

shift_vals = [0, 262, 583, 874]
interval_vals = [500, 250, 160] 
moving_averages_sets = [[9,21], [9,50], [21,100], [21,200], [50,200]]
ma_method = 'TMA'
cnt_t = 0
for  shift_val in shift_vals:
	for interval_val in interval_vals:
		for moving_averages in moving_averages_sets:
			cnt_t += 1
			ema_short = '%s_%i'%(ma_method,moving_averages[0])
			ema_long = '%s_%i'%(ma_method,moving_averages[1])
			directory = 'output/%s_%i_%i_%s_%s'%(today_date, interval_val, shift_val,ema_long,ema_short)
			if not os.path.exists(directory):
				os.makedirs(directory)
			if os.path.exists(directory+'.csv'):
				print(cnt_t,shift_val,interval_val,moving_averages, ': Processed')
			else:	
				print(cnt_t,shift_val,interval_val,moving_averages)
				run_compare(shift_val, interval_val, moving_averages, directory)
			
