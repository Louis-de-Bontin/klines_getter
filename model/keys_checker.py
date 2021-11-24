from binance.client import Client
import control.functions as func
# Create the fine keys.py wich doesn't exists on github for security reasons
func.create_file('./settings/keys.py', "API_key = ''\nAPI_secret = ''")
from settings import keys
import importlib

class Keys_checker:
    def __init__(self, menu):
        '''
        If keys are empty, asks the user to create new ones,
        otherwise, take the existing ones as parameter.
        '''
        if keys.API_key == "" and keys.API_secret == "":
            self.keys_creator(menu)
        else:
            self.API_key = keys.API_key
            self.API_secret = keys.API_secret

    def test_conexion(self):
        '''
        Conexion to the Binance API and return an asset balance to see if the keys are accepted
        '''
        self.client = Client(self.API_key, self.API_secret)
        self.infos = self.client.get_account()

    def keys_creator(self, menu, keys_allowed=True):
        '''
        Asks the user for his keys then save them.
        '''
        API_keys = menu.display_keys_asker()
        self.API_key = API_keys[0]
        self.API_secret = API_keys[1]
        self.create_keys()

    def create_keys(self):
        '''
        Write the keys in the keys.py file.
        '''
        with open('./settings/keys.py', 'w') as f:
            f.write(
                'API_key = \'' + self.API_key + '\'\n' +
                'API_secret = \'' + self.API_secret + '\'' 
            )

    def check_keys(self, menu):
        '''
        Try the keys by calling the test_conexion method.
        If it works, inform the user.
        If it doesn't, ask for new keys.
        '''
        try:
            # Update the keys package
            importlib.reload(keys)
            self.test_conexion()
            print('Keys are valid and working.\n\n')
            return False
        except Exception as e:
            print(
                'The keys you have entered aren\'t allowed by binance.' +
                'Because : ' + str(e) +
                '\nPlease try again.')
            # Update the file keys.py
            self.keys_creator(menu, keys_allowed=False)
            return True
