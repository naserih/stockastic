# 5_compare_ema.py
from tools import *
import env

database_path = env.database_path
sorted_by_median_path = env.sorted_by_median_path
sorted_by_mean_path = env.sorted_by_mean_path 


index_ticker = 'index_GSPTSE'

tickers_sorted = read_sorted_files_csv(sorted_by_median_path)
tickers_sorted.append(index_ticker)
tickers_dic = get_tickers_dic(database_path)

out_plots = './output/plots'
out_csvs = './output/gain_csvs'
if not os.path.exists(out_csvs):
	os.makedirs(out_csvs)
if not os.path.exists(out_plots):
	os.makedirs(out_plots)

def run_compare(shift_val, interval_val, moving_averages, file_name):
	directory = '%s/%s'%(out_plots,file_name)
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
			if not os.path.exists('%s/%s/%s.png'%(out_plots,file_name,title)):
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
				plt_save(plot, '%s/%s/%s.png'%(out_plots,file_name,title))
			# print(cnt, ticker, '%5.0f%%'%gain_value, end="")
			# else:
			# 	print('saved!')
		except:
			print ('plot failed: \t', title)
		# if cnt%10 == 0:
		# 	print("|")
	# plot.close('all')
	write_to_csv(gains,'%s/%s.csv'%(out_csvs,file_name))



today_date = '2019-02-22' # start of prediction
# shift_val = 0 # trade days difference between fix and moving
# interval_val = 160 # duration o the comparision
# moving_averages = [21,200] #

shift_vals = [0, 262, 583, 874]
interval_vals = [500, 250, 160] 
moving_averages_sets = [[9,21], [9,50], [21,100], [21,200], [50,200]][:1]
ma_method = 'EMA'
cnt_t = 0
for  shift_val in shift_vals:
	for interval_val in interval_vals:
		for moving_averages in moving_averages_sets:
			cnt_t += 1
			ema_short = '%s_%i'%(ma_method,moving_averages[0])
			ema_long = '%s_%i'%(ma_method,moving_averages[1])
			file_name = '%s_%i_%i_%s_%s'%(today_date, interval_val, shift_val,ema_long,ema_short)
			if os.path.exists('%s/%s.csv'%(out_csvs,file_name)):
				print(cnt_t,shift_val,interval_val,moving_averages, ': Processed')
			else:	
				print(cnt_t,shift_val,interval_val,moving_averages)
				run_compare(shift_val, interval_val, moving_averages, file_name)
			
