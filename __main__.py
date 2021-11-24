from display.menus import Menus
from model.keys_checker import Keys_checker
from model.binance_spot import Binance_spot

def main():
    menu = Menus()
    what_to_do = menu.display_main()
    
    # This function  check if there is API keys, and if they are usable.
    # If not, the user must enter new ones.

    ######################
    #### Should call functions from ./control/ instead of controling
    ######################
    if what_to_do == 1:
        '''
        User wants to create new keys or check validity of saved keys.
        Creats an instance of key_ckecker, and check keys until they work.
        '''
        check_key = Keys_checker(menu)
        keep_going = True
        while keep_going == True:
            keep_going = check_key.check_keys(menu)
    elif what_to_do == 2:
        '''
        User wants to download klines from binance spot.
        Ask the user for settings, the instanciate Binance_spot with those settings.
        '''
        settings = menu.display_pairs_asker()
        spot_klines = Binance_spot(
            settings['pairs'],
            settings['datestart'],
            settings['dateend'],
            settings['timeframes']
        )
    elif what_to_do == 3:
        pass

if __name__ == '__main__':
    main()
