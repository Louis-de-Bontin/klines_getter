from binance.client import Client

import pandas as pd

class Binance_spot():
    def test_conexion(self, API_key, API_secret):
        '''
        Conexion to the Binance API and return an asset balance to see if the keys are accepted
        '''
        self.client = Client(API_key, API_secret)
        self.infos = self.client.get_account()
