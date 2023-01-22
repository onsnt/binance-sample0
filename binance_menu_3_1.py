#from binance_init import *
from binance_history_download_csv import *
import binance_ta as ta
import binance_menu_0 as menu0
#import os

menu_options = {
    0: 'Previos menu',  
    1: 'Plot hourly graph',
    2: 'Plot daily procent change graph',
}

def print_menu3():
    #Attention os specific
    #clear = lambda: os.system('cls')
    #clear()    
    
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )
    
def option31():
    print('Plot hourly graph')
    ta.plot_graph_ta('hourly')

def option32():
    print('Plot daily procent change graph')
    ta.plot_graph_ta('procent')

def option33():
    pass

def get_choice_menu3():
    while(True):
        print_menu3()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        
        if option == 0:
            print('Return to main menu')
            break
 
        elif option == 1:
            option31()
           
        elif option == 2:
            option32()
            
        elif option == 3:
            option33()
            
        else:
            print('Invalid option. Please enter a number between 1 and 2.')
    menu0.print_menu()