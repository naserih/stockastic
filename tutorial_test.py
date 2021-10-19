import os
mypath = './data/TSX'
onlyfiles = [f for f in os.listdir(mypath) if ".csv" in f]
ticker_dic = {}
for filename in onlyfiles:
  ticker_dic[filename[:-4]] = {'filepath':os.path.join(mypath, filename)}

plt.figure(figsize=(18,9))
plt.grid()
plt.plot(range(len_fix), fix_stock, '-k')
plt.plot(range(len_fix), model_stock,'-m') 
    