#optimized_EMA_ratio.py
from tools import *

gain_filepath = './output/gain_csvs/'
files = [f for f in os.listdir(gain_filepath) if ".csv" in f and 'merged' not in f]
# print(files)

ema_gain_matrix  = {}
reg_gain_matrix = {}
beta_matrix = {}
for filename in files:
	fileinfo = filename[:-4].split('_')
	# print(fileinfo)
	today_date = fileinfo[0]
	interval = fileinfo[1]
	shift = fileinfo[2]
	long_ema = fileinfo[4]
	short_ema = fileinfo[6]
	df = read_csv_as_df(os.path.join(gain_filepath,filename))
	# print(df.columns)
	ema_gain_matrix['ticker'] = df['ticker']
	ema_gain_matrix["_".join(fileinfo[1:])] = df['ema_gain']
	beta_matrix['ticker'] = df['ticker']
	beta_matrix["_".join(fileinfo[1:])] = df['beta_coef']
	reg_gain_matrix['ticker'] = df['ticker']
	reg_gain_matrix["_".join(fileinfo[1:])] = df['normal_gain']

reg_gain_df  = pd.DataFrame(data=reg_gain_matrix)
ema_gain_df  = pd.DataFrame(data=ema_gain_matrix)
beta_df  = pd.DataFrame(data=beta_matrix)

# [9,21], [9,50], [21,100], [21,200], [50,200]
ema = 'EMA_200_EMA_50'
median_gain = [['col_name', 'median_y_gain']]
for col in ema_gain_df.columns:
	if ema in col:
		col_info = col.split("_")
		interval = int(col_info[0])
		shift = int(col_info[1])
		inx_rate = 253/interval
		x = beta_df[col]
		y = ((1+ema_gain_df[col]/100)**inx_rate-1)*100
		median_gain.append([col,np.median(y)])

# print(median_gain)
write_to_csv(median_gain, '%s/median_gain_%s.csv'%('output',ema))


inx0 = '160_0_EMA_21_EMA_9'
inx1 = '250_0_EMA_21_EMA_9'
inx2 = '500_0_EMA_21_EMA_9'

inx0_rate = 253/160
inx1_rate = 253/250
inx2_rate = 253/500

title = 'beta VS gain'
x0 = beta_df[inx0]
y0 = ((1+ema_gain_matrix[inx0]/100)**inx0_rate-1)*100
x1 = beta_df[inx1]
y1 = ((1+ema_gain_matrix[inx1]/100)**inx1_rate-1)*100
x2 = beta_df[inx2]
y2 = ((1+ema_gain_matrix[inx2]/100)**inx2_rate-1)*100

# x1 = beta_df[inx2]
# y1 = ema_gain_matrix[inx2]*inx2_rate
# y1 = ((1+ema_gain_matrix[inx1]/100)**inx1_rate-1)*100
# y2 = ((1+ema_gain_matrix[inx2]/100)**inx2_rate-1)*100

legends = ['ema_gain_160:%6.2f'%np.median(y0), 'ema_gain_250:%6.2f'%np.median(y1), 'ema_gain_500:%6.2f'%np.median(y2)]

plot = plot_stocks([x2, x1,x0],[y2,y1,y0],
					markers=['s', 'o', 'D'],
					linestyles=['None', 'None', 'None'],
					legends=legends,
					title= title
					)

outpath = './output/plots/0_medianGain_'+inx0[4:]	
# plt_show(plot)
plt_save(plot, outpath)
# plt.hist(y0, bins=100, alpha=0.3)
# plt.hist(y1, bins=100, alpha=0.3)
# plt.hist(y2, bins=100, alpha=0.3)
# print(np.mean(y2), np.median(y2))
# plt.show()
# print(merged_df.columns)
# ema_gain_df.to_csv('./merged_ema_gain_files.csv')
# reg_gain_df.to_csv('./merged_reg_gain_files.csv')
# beta_df.to_csv('./merged_beta_files.csv')

