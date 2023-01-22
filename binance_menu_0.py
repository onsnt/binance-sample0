import binance_init as b_init
import binance_history_download_csv as dl
import binance_menu_2_1 as menu2
import binance_menu_3_1 as menu3
import binance_menu_4_1 as menu4

menu_options = {
    0: 'Exit',
    1: 'Download history',
    2: 'ML',
    3: 'Plot TA',
    4: 'Order',
    5: 'First init (for ML)',
}


def print_menu():
    print('-------')
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


def option1():
    print('Get download parametr`s from cfg')
    dl.download_csv()
    print('Download history complete')


def option5():
    b_init.binance_init()
    print('init script done')


if __name__ == '__main__':
    while (True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')

        if option == 0:
            print('Thanks. Bye')
            exit()

        elif option == 1:
            option1()

        elif option == 2:
            menu2.get_choice_menu2()

        elif option == 3:
            menu3.get_choice_menu3()

        elif option == 4:
            menu4.get_choice_menu4()

        elif option == 5:
            option5()

        else:
            print('Invalid option. Please enter a number between 1 and 4.')
