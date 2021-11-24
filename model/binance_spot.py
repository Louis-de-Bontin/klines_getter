from binance.client import Client
import pandas as pd

class Binance_spot():
    def __init__(self, pairs, datestart, dateend, timeframes):
        self.pairs = pairs
        self.datestart = datestart
        self.dateend = dateend
        self.timeframes = timeframes

    def get_spot_klines(self):
        pass

    def save_spot_klines_as_csv(self):
        pass
    
    def build_df_from_csv(self):
        pass
