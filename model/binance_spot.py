from binance.client import Client
import control.functions as func
# Create the fine keys.py wich doesn't exists on github for security reasons
from settings import build, keys
import pandas as pd
from datetime import datetime

class Binance_spot():
    def __init__(self):
        self.API_key = keys.API_key
        self.API_secret = keys.API_secret
        self.client = Client(self.API_key, keys.API_secret)

        self.get_all_pairs()
    
    def get_all_pairs(self):
        '''
        Get all tickers to have a ref, so user can only enter existing pairs.
        '''
        tickers = self.client.get_all_tickers()
        self.all_pairs = []
        for ticker in tickers:
            self.all_pairs.append(ticker['symbol'])
    
    def display_pairs_asker(self):
        '''
        Ask the user about the settings he need for the klines download.
        Pairs, datestart, dateend, timeframe
        '''
        self.pairs = []
        self.timeframes = []
        timeframes_possibilities = ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '1w', '1M']

        print('Enter the pair you want to collect (format PAIR1PAIR2, ex:BTCUSDT), then press enter.')
        print('Press enter when you\'re done.')
        while True:
            user_entry = input('Pair : ').upper()
            if user_entry != '' and user_entry in self.all_pairs:
                self.pairs.append(user_entry)
            elif user_entry != '':
                print('This pair doesn\'t exists on Binance, try again.')
            else:
                if len(self.pairs) == 0:
                    print('Pairs list can\'t be empty. Try again.')
                else:
                    break
        self.ask_date()
        tdelta = self.dateend - self.datestart
        if tdelta.total_seconds() < 86400:
            print('Start date more recent than end date. Please enter valid dates.')
            dates = self.ask_date()
        
        print('Enter timeframes (possibilities : 5m, 15m, 30m, 1h, 4h, 12h, 1d, 1w, 1M)')
        while True:
            user_entry = input('Timeframe : ')
            if user_entry != '':
                if user_entry in timeframes_possibilities:
                    self.timeframes.append(user_entry)
                    timeframes_possibilities.remove(user_entry)
                else:
                    print('Invalid entry, try again.')
            else:
                if len(self.timeframes) == 0:
                    print('\nTimeframe list can\'t be empty. Try again.')
                else:
                    break
    
    def ask_date(self):
        '''
        Ask the user for date start and date end, and check the format.
        '''
        now = datetime.now()
        print('\nEnter the start date (format YY/MM/DD) : ')
        while True:
            try:
                entry_user = datetime.strptime(input(), '%y/%m/%d')
                tdelta = now - entry_user
                if tdelta.total_seconds() <= 0:
                    print('Date is in the future. Try again :')
                else:
                    self.datestart = entry_user
                    break
                continue
            except Exception as e:
                print(e)
                print('\nDate start :\nInvalid date format, try again (format YY/MM/DD):')
                continue
        print('\nEnter the end date (format YY/MM/DD or \'now\') : ')
        while True:
            entry_user = input()
            if entry_user.lower() == 'now':
                self.dateend = datetime.now()
                break
            else:
                entry_user = datetime.strptime(entry_user, '%y/%m/%d')
                try:
                    tdelta = now - entry_user
                    if tdelta.total_seconds() <= 0:
                        print('Date is in the future. Try again :')
                    else:
                        self.dateend = entry_user
                        break
                    continue
                except:
                    print('\nDate end : \nInvalid date format, try again (format YY/MM/DD):')
                    continue
        self.deltadays = self.dateend - self.datestart
        print(self.deltadays)
        self.deltadays = self.deltadays.total_seconds()/86400
        print(self.deltadays)

    def interpret_user_entries(self):
        '''
        Transfor the user entries in values readable by python-binance
        '''
        self.binance_datestart = func.date_to_binance_format(self.datestart)
        self.binance_dateend = func.date_to_binance_format(self.dateend)

    def get_spot_klines(self):
        ##########
        my_dict = {
            'pair1': {
                'tf1' : 'table',
                'tf2' : 'table'
            },
            'pair2' : {
                'tf1' : 'table',
                'tf2' : 'table'
            }
        }
        ########
        self.interpret_user_entries()
        self.dict_of_tables = {}
        for pair in self.pairs:
            func.create_folder('data/02_intermediate/data_price/binance/futures/' + pair)
            self.dict_of_tables[pair] = {}
            for timeframe in self.timeframes:
                candles = self.client.get_historical_klines(pair, timeframe, self.binance_datestart, self.binance_dateend)
                self.process_candles()
                self.dict_of_tables[pair][timeframe] = candles
                # for candle in candles:
                #     print(candle)
                print(self.dict_of_tables)
            print('#########\n\n##########')

    def process_candles(self):
        pass

    def save_spot_klines_as_csv(self):
        pass
    
    def build_df_from_csv(self):
        pass
