import os

def create_file(path, content):
    '''
    Create a new file, withe the full path (name included) and the content.
    '''
    if not os.path.isfile(path):
        with open(path, 'w') as f:
            f.write(content)

def create_folder(path):
    if not os.path.isdir(path):
        os.mkdir(path)

def timeframe(Client, interval):
    if interval == '1m':
        return Client.KLINE_INTERVAL_1MINUTE
    if interval == '3m':
        return Client.KLINE_INTERVAL_3MINUTE
    elif interval == "5m":
        return Client.KLINE_INTERVAL_5MINUTE
    elif interval == "15m":
        return Client.KLINE_INTERVAL_15MINUTE
    elif interval == "30m":
        return Client.KLINE_INTERVAL_30MINUTE
    elif interval == "1h":
        return Client.KLINE_INTERVAL_1HOUR
    elif interval == "2h":
        return Client.KLINE_INTERVAL_2HOUR
    elif interval == "4h":
        return Client.KLINE_INTERVAL_4HOUR
    elif interval == "6h":
        return Client.KLINE_INTERVAL_6HOUR
    elif interval == "8h":
        return Client.KLINE_INTERVAL_8HOUR
    elif interval == "12h":
        return Client.KLINE_INTERVAL_12HOUR
    elif interval == "1d":
        return Client.KLINE_INTERVAL_1DAY
    elif interval == "3d":
        return Client.KLINE_INTERVAL_3DAY
    elif interval == "1w":
        return Client.KLINE_INTERVAL_1WEEK
    elif interval == '1M':
        return Client.KLINE_INTERVAL_1MONTH

def date_to_binance_format(date):
    date = str(date)
    mois_int = int(date[5] + date[6])
    if mois_int == 1:
        mois = "Jan"
    elif mois_int == 2:
        mois = "Feb"
    elif mois_int == 3:
        mois = "Mar"
    elif mois_int == 4:
        mois = "Avr"
    elif mois_int == 5:
        mois = "May"
    elif mois_int == 6:
        mois = "Jun"
    elif mois_int == 7:
        mois = "Jul"
    elif mois_int == 8:
        mois = "Aou"
    elif mois_int == 9:
        mois = "Sep"
    elif mois_int == 10:
        mois = "Oct"
    elif mois_int == 11:
        mois = "Nov"
    elif mois_int == 12:
        mois = "Dec"
    return date[8] + date[9] + " " + mois + ", " + date[0] + date[1] + date[2] + date[3]

def date_binance_format_to_python_compatible(date):
    pass