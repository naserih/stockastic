# stockastic
Stock Data Science With Python
## introduction
This is a startup project to test some of the data science tools on stock data in order to find meaningful trends.
## Requirements: Starting with python
- You will need a git installed on your machine.
- You will require Phython 3 on your machine with working version of pip3 to start this project
- you can check versions of python and pip using any of the following comments: `python --version`, `python3 --version`, `pip --version`, `pip3 --version`
- Clone the current repository `git clone https://github.com/hn617/stockastic.git`
- `cd stockastic`
- make a new gir branch `git checkout -b lesson1`
- `pip3 install -r requirements`
- make sure you have all the requirements installed into the python3

## Lesson 1: Read data from file into the pandadata frame

<details>
<summary> Read data from CSV file ...   </summary>   
  
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
    ticker_dic[filename[:-4]] = os.path.join(mypath, filename)
```
  2. Write function to read a CSV file for a given ticker as a panda dataframe. [HELP](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html)
    ```
  import pandas as pd
  pd.read_csv("full_path_to_csv_file")
```
  3. Write a function to return the `mean` of the stock `Volumes` for a input ticker.
  
  ```
  function(ticker):
    mean_volume = ... //finds mean volume
    return mean_volume
  ```
  4. Modify the function to return the `mean` of the last 60 stock volumes.
  5. Save stock ticker and mean volume as a tupple and push it into a array.
  
  ```
  array = []
  array.push((ticker, mean_volume))
  ```
  5. sort the array by volume 
  6. Write a function to write top 100 stockes with their mean volumes into a csv file 
 </details>

## Lesson 2: Visualize Data in matplotlib
<details> 
  <summary>Visualize Data in matplotlib  </summary> 
  ###
</details>

## Lesson 3: Export selected Data in CSV
<details>
  <summary>Export selected Data in CSV...  </summary> 
</details>

## Lesson 3: Export selected Data in CSV
<details>
  <summary> Sort Stock Symbols by Volume </summary> 
</details>

  ## Lesson 5: Fit data with linear models
<details>
<summary> Fit data with linear models  </summary> 
</details>

## Lesson 6: Download data from API
<details>
<summary> Download data from API  </summary> 
</details>

