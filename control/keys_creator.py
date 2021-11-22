import os.path
import importlib

def keys_creator(menu, keys_allowed=True):
    '''
    Check if the keys.py file exists.
    If not, create it, if the keys are not allowed, it modifies it.
    '''

    if not os.path.isfile('./settings/keys.py') or keys_allowed == False:
        API_keys = menu.display_keys_asker()
        create_keys(API_keys)
    check_keys(menu)

def create_keys(API_keys):
    '''
    Write the keys in the keys.py file.
    '''

    with open('./settings/keys.py', 'w') as f:
        f.write(
            'API_key = \'' + API_keys[0] + '\'\n' +
            'API_secret = \'' + API_keys[1] + '\'' 
        )

def check_keys(menu):
    '''
    Try the keys by creating an instance of binance spot.
    '''

    from model.binance_spot import Binance_spot
    from settings import keys
    try:
        # Update the keys package
        importlib.reload(keys)
        session = Binance_spot()
        session.test_conexion(keys.API_key, keys.API_secret)
        print('Keys are valid and working.\n\n')
    except Exception as e:
        print(
            'The keys you have entered aren\'t allowed by binance.' +
            'Because : ' + e +
            '\nPlease try again.')
        # Update the file keys.py
        keys_creator(menu, keys_allowed=False)
