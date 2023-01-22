import binance_menu_0 as menu0
import binance_ml as b_ml


menu_options = {
    0: 'Previos menu',  
    1: 'Analyse',
    2: 'Load model',
    3: 'Save model',
}

def print_menu2():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def option21():
    print('Analyse')
    b_ml.regressionmodel()

def option22():
    pass

def option23():
    pass

def get_choice_menu2():
    while(True):
        print_menu2()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        
        if option == 0:
            print('Return to main menu')
            break
 
        elif option == 1:
            option21()
           
        elif option == 2:
            option22()

        elif option == 3:
            option23()            
        else:
            print('Invalid option. Please enter a number between 1 and 3.')
    menu0.print_menu()