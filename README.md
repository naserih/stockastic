# stockastic
Stock Data Science With Python
## introduction
This is a startup project to test some of the data science tools on stock data to find meaningful trends.
## Requirements: Starting with python
- You will need a git installed on your machine.
- You will require Python 3 on your machine with a working version of pip3 to start this project
- you can check versions of python and pip using any of the following comments: `python --version`, `python3 --version`, `pip --version`, `pip3 --version`
- Clone the current repository `git clone https://github.com/hn617/stockastic.git`
- `cd stockastic`
- make a new git branch `git checkout -b lesson1`
- `pip3 install -r requirements`
- make sure you have all the requirements installed into the python3
- Learn about TSX stock tickers and daily stock prices (open, close), and volume. 

## Lesson 1: Read data from a file into the pandas' data frame

In this lesson, we are going to build a python script to read TSX historical stock prices (2019-2020) and sort the stock tickers according to their average volume.
<details>
<summary> Read data from CSV file ...   </summary>   
  
  0. data directory contains daily stock values for TSX stocks for the year 2019-2020. Files' names are stock tickers. Open a couple of the CSV files and check the data structure. We are going to create a ticker dictionary containing file path and stock details. 
```
  ticker_dic = {'<TIKER_0>' : {
                              'FILE_PATH': '<full_path_to_ticker_0_file>'},
                              'mean_volume' : xx,
                              'order_volume' : xx,
                              },
                 '<TIKER_1>' : {
                              'FILE_PATH': '<full_path_to_ticker_1_file>'},
                              'mean_volume' : xx,
                              'order_volume' : xx,
                              }
```
  later we will add fore data into the ticker dictionary.
  1. Use python to list all the CSV files (stock tickers) from `./data/TSX/20190222`
```
import os
mypath = ""
onlyfiles = [f for f in os.listdir(mypath) if ".csv" in f]
```
  Then create a dictionary with ticker name as key and full file path to the csv file as value. You can do something like.
```
ticker_dic = {}
for filename in onlyfiles:
  ticker_dic[filename[:-4]] = {'filepath':os.path.join(mypath, filename)}
```
  2. Write a function to read a CSV file for a given ticker as a panda dataframe. [HELP](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html)
  
``` 
import pandas as pd
  import json
df = pd.read_csv("full_path_to_csv_file", header=0,sep=",", thousands=',', index_col=None, parse_dates=['Date'])
if len(df['Volume']) == 0:
  del ticker_dic[ticker]
```
  3. Write a function to return the `mean` of the stock `Volumes` for a input ticker. `df.mean(axis=0)`

```
  def get_mean_volume(ticker):
    mean_volume = ... //finds mean volume
    return mean_volume
```
  4. Modify the function to add the mean_volume into the ticker_dic.

```
    ticker_dic[ticker]['mean_volume'] = mean_volume
```
  5. sort tickers by their mean_volume and add the ticker order to the ticker_dic

```
  sorted_by_volume = sorted(ticker_dic, key=lambda k: ticker_dic[k]['mean_volume'], reverse=True)
  # check to make sure it is working 
  print (sorted_by_volume)
  for i in range(len(sorted_by_volume)):
      ticker = sorted_by_volume[i]
      order_volume = i
      ticker_dic[ticker]['order_volume'] = order_volume
```
 </details>

## Lesson 2: Visualize Data in matplotlib
 
In this lesson we will add stock `open` and `close` arrays into the `ticker_dic` and plot stock values for some of high volume tickers.
<details> 
<summary>Visualize Data in matplotlib  </summary> 

  1. Similar to the previous lesson, add `median_volume` and `order_median_volume` into the ticker dictionary.
  
  2. Create panda array with ticker's `order_median_volume`, `order_mean_volume`, `median_volume`, and `mean_volume`.
 
```
df = pd.DataFrame(tickers_dic.values())
```
  3. plot stock `mean_volume` and `median_volume` vs `order_volume`
 
```
 df.plot(x='order_median_volume', y='median_volume')
```
  ###
</details>

## Lesson 3: Compare Open and Close values

  In this lesson, we will work with stock Open and Close values. We will investigate the correlation between Close and Open values of the stock.
<details>
  <summary>Compare stock Open to its previous Close    </summary> 
  
  1. For a given ticker in `tickers_dic` calculate the ratio between `Adj. Close` and `Open` for each row and store them as a new column `C/O`.
  2. calculate the ratio between `Open` and the previous day's `Adj. Close` values for each row and store them as a new column `O/C`.
  3. Plot `O/C` vs `C/O`
 
```

ticker = 'AC.TO'
close_open_ratio = tickers_dic[ticker]['df']['Adj. Close'] / tickers_dic[ticker]['df']['Open'] 
tickers_dic[ticker]['df']['C/O'] = close_open_ratio
open_close_ratio =   tickers_dic[ticker]['df']['Open'] / tickers_dic[ticker]['df']['Adj. Close'].shift(1)
tickers_dic[ticker]['df']['O/C'] = open_close_ratio
df.plot(x='C/O', y='O/C')
```
  
</details>

## Lesson 4: Compare two stock values

  In this lesson we want to build a function to allow us to compare stock `Adj. Close` values for two tickers.

  <details>
<summary> Comparing two stocks </summary> 

  We want to define a function to get tickers_dic, fixed_ticker, moving_ticker, interval, time_shift,  today_date, forecast_days and return plot the fix_ticker_value vs mocinv_ticker_value.
  
    fixed_ticker: is a base ticker that we want to forecast. 

    moving_ticker: is a ticker that we want to compare to fixed_ticker and use for forecasting.
  
    interval: is the time interval that we want to compare two stocks. For example 60 business days (~three months).
  
    time_shift: is a shift between the fixed_ticker snd moving_ticker.
  
    today_date: date for the start of forecasting. In reality, this will be today's date but for training, we will change this date and test the forecasting.
    
    forecast_days: number of the days from today_date that we want to forecast.
    
    Note: If the today_date is the last available date for fixed_ticker then time_shift should be greater than the forecast_days. For example, if we want to forecast the next 10 business days (forecast_days = 10) then time_shift should be greater than 10.
    
1. define a function with the requested parameters:
  ```
  def compare_stocks(tickers_dic, fixed_ticker, moving_ticker, interval, time_shift, today_date, forecast_days) 
  ```
 2. read dfs for both fixed and moving tickers 
 3. convert `Date` column to datetime.date object. Similarly, convert the `today_date` string to the datetime.date object.
 4. normalize the 'Adj. Close' values of both stocks using z-score (standardized). Store the normalization parameters to allow us to convert the normalized values back to the 
 5. filter the fixed_ticker df to read the number of `interval` rows starting from `today_date` 
 6. filter the moving_ticker df to read the number of  `interval`+`time_shift` rows starting from `today_date` 
 7. plot normilied 'Adj. Close' values for both  fixed_ticker and shifted moving_ticker
</details>

  ## Lesson 5: Calculate beta value and moving averages. 
<details>
<summary>  Calculate beta value and moving averages.  </summary> 
'''
- get TSX index [DONE: data/index_GSPTSE.csv]
- read GSPTSE index as df
- compare index_GSPTSE to the fixed ticker
- calculate beta value: covariance(TICKER,GSPTSE)/variance(GSPTSE)
- calculate simple moving average (SMA)
- compare 50-200 day SMA
- compare 15-50 days SMA [DONE]
- calculate exponential moving average (EMA) [DONE!]
'''

</details>


## Lesson 6: Compare moving averages
<details>
<summary> Download data from API  </summary> 
</details>

## Lesson 7: forcast by comparing two stocks
<details>
<summary> Download data from API  </summary> 
</details>

## Lesson 8: Download data from API
<details>
<summary> Download data from API  </summary> 
</details>

