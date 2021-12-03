from binance.client import Client
import control.functions as func
# Create the fine keys.py wich doesn't exists on github for security reasons
from settings import build, keys
import pandas as pd
from datetime import datetime, timezone

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
                func.create_folder('data/02_intermediate/data_price/binance/spot/' + user_entry)
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
            self.ask_date()
        
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
                self.dateend = now
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
        self.deltadays = self.deltadays.total_seconds()/86400

    def interpret_user_entries(self):
        '''
        Transfor the user entries in values readable by python-binance
        '''
        self.binance_datestart = func.date_to_binance_format(self.datestart)
        self.binance_dateend = func.date_to_binance_format(self.dateend)

    def get_spot_klines(self):
        '''
        Download the klines and build a dictionary with all the klines lists.
        '''
        self.interpret_user_entries()
        self.dict_of_tables = {}
        for pair in self.pairs:
            func.create_date_folder(pair, self.datestart, self.dateend)
            for timeframe in self.timeframes:
                candles = self.client.get_historical_klines(pair, timeframe, self.binance_datestart, self.binance_dateend)
                ohlc = self.process_candle(candles)
                self.save_ohlc(ohlc, pair, 'BN', 'spot', timeframe)
    
    def save_ohlc(self, full_df, pair, exchange, marketplace, timeframe):
        '''
        This function manipulates the dataframe, split it by years, then split all the new ones by months, and again by day.
        Then, it builds the PATH and the CSV files names, and save the ohlc in the data.
        '''
        full_df['year'] = full_df['Date Open'].dt.year
        full_df['month'] = full_df['Date Open'].dt.month
        full_df['day'] = full_df['Date Open'].dt.day
        # Split by years
        df_year = [full_df[full_df['year'] == y] for y in full_df['year'].unique()]

        for df in df_year:
            # Split by months
            df_month = [df[df['month'] == m] for m in df['month'].unique()]

            for dataframe in df_month:
                # Split by days
                df_day = [dataframe[dataframe['day'] == d] for d in df['day'].unique()]

                for ohlc in df_day:
                    # Try/except because some df can be empty : only 1 weekly candle per 7 days.
                    try:
                        month = str(ohlc.iloc[-1]['month'])
                        year = str(ohlc.iloc[-1]['year'])
                        day = str(ohlc.iloc[-1]['day'])
                        if len(month) == 1:
                            month = '0' + month
                        year_month = year + month

                        PATH = 'data/02_intermediate/data_price/binance/' + marketplace + '/' + pair + '/' + year_month + '/'
                        FILE_NAME = exchange + '_' + pair + '_ohlc_' + year + month + day + '_' + timeframe + '.csv'

                        ohlc.to_csv(PATH + FILE_NAME, index=False)
                    except:
                        continue     

    def process_candle(self, candles):
        '''
        Set the timezone, and the columns names.
        '''
        for candle in candles:
            candle[0] = datetime.fromtimestamp(candle[0]/1000, tz=timezone.utc)
            candle[6] = datetime.fromtimestamp(candle[6]/1000, tz=timezone.utc)
        ohlc = pd.DataFrame(candles)
        ohlc = ohlc.rename(columns= {
            0: "Date Open",
            1: "Open",
            2: "High",
            3: "Low",
            4: "Close",
            5: "Volume",
            6: "Date Close",
            7: "Quote",
            8: "Nb of trades",
            9: 'Taker buy base asset volume',
            10: 'Taker buy quote asset volume',
            11: 'Ignore'
        })
        return ohlc
    
    def build_df_from_csv(self, pair, timeframe):
        # Regarde si les data sont dispo, sinon il les dl
        # Si, par exemple, des data sont dispo du 2021/06/01, jusqu'au 2021/10/01,
        # mais que nous sommes le 2021/11/01, il dl la différence.
        pass
