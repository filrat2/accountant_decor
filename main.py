# -*- coding: utf-8 -*-

# import needed functions / modules
from manager import manager

# define variables
manager.execute('whs_read', manager.store, manager.store_filepath)

# define account balance (import from file)
manager.account_balance = manager.execute('acc_read',
                                          manager.account_balance_filepath)

# %% MAIN LOOP

while True:
    command = input("Podaj komendę (sprzedaz/kupno/magazyn/saldo/konto/raport"
                    "/exit): ")
    command = ''.join(filter(str.isalpha, command)).lower()

    if command == "exit":
        manager.execute('acc_write', manager.account_balance,
                        manager.account_balance_filepath)
        manager.execute('whs_write', manager.store, manager.store_filepath)
        break

    elif command == "sprzedaz":
        product_name = input("Nazwa towaru: ").lower()
        manager.account_balance = manager.execute('sprzedaz', product_name,
                                                  manager.store,
                                                  manager.account_balance,
                                                  manager.operation_history)

    elif command == "kupno":
        product_name = input("Nazwa towaru: ").lower()
        manager.account_balance = manager.execute('kupno', product_name,
                                                  manager.store,
                                                  manager.account_balance,
                                                  manager.operation_history)

    elif command == "magazyn":
        product_name = input("Nazwa towaru: ").lower()
        manager.execute('whs_check',  product_name, manager.store,
                        manager.operation_history)

    elif command == "saldo":
        manager.account_balance = manager.execute('acc_change',
                                                  manager.account_balance,
                                                  manager.operation_history)

    elif command == "konto":
        manager.execute('acc_display', manager.account_balance)

    elif command == "raport":
        manager.execute('raport', manager.operation_history)

    else:
        print("Niepoprawna komenda!\n"
              "Dozwolone komendy to 'sprzedaz', 'kupno', 'magazyn','saldo', "
              "'konto', 'raport', 'exit'.")
        pass

# %%
