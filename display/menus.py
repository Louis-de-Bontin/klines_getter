from datetime import datetime

class Menus():
    def display_main(self):
        '''
        Display the main menu and allow the user to interact with the program
        '''
        print(
            'What do you want to do ?\n' +
            '1) Check if my keys work\n' +
            '2) Download spot klines\n' +
            '3) Download futures klines\n'
        )
        user_choice = input()
        if user_choice not in ['1', '2', '3']:
            print('\nInvalid entry, try again.\n')
            user_choice = self.display_main()
        
        return int(user_choice)

    def display_keys_asker(self):
        '''
        If the user has no keys, or if they are rejected by binance, new keys are requested.
        '''

        print(
            'This package needs your biance API key and API secret to continue.\n' +
            'They will remain private and be asked only once.\n' +
            'If you need to modify them, you can do it manually by editing the settings/keys.py file'
        )
        API_key = str(input('Enter your Binance API key : '))
        API_secret = str(input('Enter your Binance API secret : '))
        print('\n\n')
        return API_key, API_secret
    
    def ask_date(self):
        '''
        Ask the user for date start and date end, and check the format.
        '''
        print('\nEnter the start date (format YY/MM/DD) : ')
        while True:
            try:
                datestart = datetime.strptime(input(), '%y/%m/%d')
                break
            except:
                print('\nDate start :\nInvalid date format, try again (format YY/MM/DD):')
                continue
        print('\nEnter the end date (format YY/MM/DD) : ')
        while True:
            entry_user = input()
            if entry_user == 'now':
                dateend = datetime.now()
            else:
                try:
                    dateend = datetime.strptime(entry_user, '%y/%m/%d')
                    break
                except:
                    print('\nDate end : \nInvalid date format, try again (format YY/MM/DD):')
                    continue
        return datestart, dateend

    def display_pairs_asker(self):
        '''
        Ask the user about the settings he need for the klines download.
        Pairs, datestart, dateend, timeframe
        '''
        pairs = []
        timeframes = []
        timeframes_possibilities = ['5m', '15m', '30m', '1h', '4h', '12h', '1d', '1w', '1M']

        print('Enter the pair you want to collect (format PAIR1PAIR2, ex:BTCUSDT), then press enter.')
        print('Press enter when you\'re done.')
        while True:
            user_entry = input('Pair : ').upper()
            if user_entry != "":
                pairs.append(user_entry)
            else:
                if len(pairs) == 0:
                    print('Pairs list can\'t be empty. Try again.')
                else:
                    break
        dates = self.ask_date()
        tdelta = dates[1] - dates[0]
        if tdelta.total_seconds() < 86401:
            print('Start date more recent than end date. Please enter valid dates.')
            dates = self.ask_date()
        
        print('Enter timeframes (possibilities : 5m, 15m, 30m, 1h, 4h, 12h, 1d, 1w, 1M)')
        while True:
            user_entry = input()
            if user_entry != '':
                if user_entry in timeframes_possibilities:
                    timeframes.append(user_entry)
                    timeframes_possibilities.remove(user_entry)
                else:
                    print('Invalid entry, try again.')
            else:
                if len(pairs) == 0:
                    print('\nPairs list can\'t be empty. Try again.')
                else:
                    break
        settings = {
            'pairs': pairs,
            'datestart': dates[0],
            'dateend': dates[1],
            'timeframes': timeframes
        }
        return settings
        