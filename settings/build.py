from control.functions import create_folder, create_file

# def build_data_folder():
folders = [
    'data',
    'data/01_raw',
    'data/02_intermediate',
    'data/03_processed',
    'data/04_models',
    'data/05_model_outputs',
    'data/06_reporting',
    'data/02_intermediate/data_price',
    'data/02_intermediate/data_price/binance',
    'data/02_intermediate/data_price/binance/spot',
    'data/02_intermediate/data_price/binance/futures'
]
for folder in folders:
    create_folder(folder)

create_file('./settings/keys.py', "API_key = ''\nAPI_secret = ''")