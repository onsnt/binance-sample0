import binance_menu_0 as menu0
import binance_depth as d
import binance_order as ordr

menu_options = {
    0: 'Previos menu',  
    1: 'Get depth',
    2: 'Open order',
    3: 'Close all opened orders',
}

def print_menu4():
    #Attention os specific
    #clear = lambda: os.system('cls')
    #clear()    
    
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def option41():
    print('Get depth')
    d.get_depth()

def option42():
    ordr.open_order()

def option43():
    ordr.close_all_order()

def get_choice_menu4():
    while(True):
        print_menu4()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        
        if option == 0:
            print('Return to main menu')
            break
 
        elif option == 1:
            option41()
           
        elif option == 2:
            option42()

        elif option == 3:
            option43()

        else:
            print('Invalid option. Please enter a number between 1 and 3.')
    menu0.print_menu()