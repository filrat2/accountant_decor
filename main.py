# -*- coding: utf-8 -*-

# import needed functions / modules

import manager

# define variables

'''
ACCOUNT_BALANCE_FILEPATH = 'account_balance.txt'
STORE_FILEPATH = 'store.csv'
operation_history = []
store = {}
'''
manager.execute('whs_read')
# read_store(store, STORE_FILEPATH)

# define account balance (import from file)
manager.execute('acc_read')
# account_balance = read_account_balance(ACCOUNT_BALANCE_FILEPATH)

# %% MAIN LOOP

while True:
    command = input("Podaj komendę (saldo/konto/raport/exit): ")
    command = ''.join(filter(str.isalpha, command)).lower()

    if command == "exit":
        manager.execute('acc_write')
        manager.execute('whs_write')
        # write_account_balance(account_balance, ACCOUNT_BALANCE_FILEPATH)
        # write_store(store, STORE_FILEPATH)
        break

    elif command == "sprzedaz":
        product_name = input("Nazwa towaru: ").lower()
        manager.execute('sprzedaz')
        # sell(product_name, store, account_balance, operation_history)

    elif command == "kupno":
        product_name = input("Nazwa towaru: ").lower()
        manager.execute('kupno')
        # buy(product_name, store, account_balance, operation_history)

    elif command == "magazyn":
        product_name = input("Nazwa towaru: ").lower()
        manager.execute('whs_check')
        # warehouse_checker(product_name, store, operation_history)

    elif command == "saldo":
        manager.execute('acc_change')
        # change_account_balance(account_balance, operation_history)

    elif command == "konto":
        manager.execute('acc_display')
        # display_account_balance(account_balance)
        print(manager.account_balance)

    elif command == "raport":
        manager.execute('raport')
        # generate_report(operation_history)

    else:
        print("Niepoprawna komenda!\n"
              "Dozwolone komendy to 'saldo', 'konto', 'raport', 'exit'.")
        pass

# %%

'''
manager.execute('whs_read')
manager.execute('whs_write')
manager.execute('whs_check')
manager.execute('acc_read')
manager.execute('acc_write')
manager.execute('acc_display')
manager.execute('acc_change')
manager.execute('kupno')
manager.execute('sprzedaz')
manager.execute('raport')
'''
