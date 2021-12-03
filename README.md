
# klines_getter
Download the historical candles of crypto on binance

# Purpose
This prompt application/package has 3 purposes :  
    -Get the historic candles of an asset named by the user on an exchange named by the user and to sort with a data analyst methodology. The user must choose a start date, an end date, futures or spot, one or more sticker, one or more timeframe.  
    -Build a pandas DataFrame from the csv built by the first feature.   
    -Get the candles in real time, this feature runs until the user, or other program stops it.  
    (When you launch it, the program will check the latest data you have on the targeted asset. It will ask if you want to dl all the historical missing datas, or if you want to choose a new startdate. If you don't have any, it will just ask the startdate, note that when you dl the last candle, python-binance ask a startdate, so it won't be that hard)

This code must be usable by prompt with a \_\_main\_\_.py to easely download the datas, and also usable as a package to impleament the 2nd and 3rd features in any trading project.  

# Architecture
<pre>
├──.gitignore  
├──README.md  
├──requirements.txt  
├──__main__.py  
├──__klines_geter__.py    
└──settings  
   ├──keys.py  
├──model  
   |--binance_spot.py  
   └──binance_futures.py  
├──display  
   ├──menus.py  
   └──errors.py  
├──control  
   ├──functions.py  
   ├──data_builder.py  
   └──csv_creator.py  
├──data  
   ├──01_raw  
   └──02_intermediate  
       └──data_price  
           └──binance  
               └──spot  
                   └──pair1  
                       ├──EXCHANGE_PAIR_ohlc_date_timeframe.csv  
                       └──...  
                   └──pair2  
                       ├──EXCHANGE_PAIR_ohlc_date_timeframe.csv  
                       └──...  
                   └──...  
   ├──03_processed  
   ├──04_models  
   ├──05_model_outputs  
   └──06_reporting  
</pre>