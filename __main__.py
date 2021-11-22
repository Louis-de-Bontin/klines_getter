from display.menus import Menus
from control import keys_creator

def main():
    menu = Menus()
    what_to_do = menu.display_main()
    
    # This function  check if there is API keys, and if they are usable.
    # If not, the user must enter new ones.
    if what_to_do == 1:
        keys_creator.keys_creator(menu)
    elif what_to_do == 2:
        pass
    elif what_to_do == 3:
        pass

if __name__ == '__main__':
    main()
