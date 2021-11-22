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
        return API_key, API_secret