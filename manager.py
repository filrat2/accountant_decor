# -*- coding: utf-8 -*-


class Manager():

    def __init__(self):
        self.account_balance_filepath = 'account_balance.txt'
        self.store_filepath = 'store.csv'
        self.operation_history = []
        self.store = {}
        self.account_balance = []
        self.actions = {}

    def assign(self, name):

        def decorate(func):
            self.actions[name] = func
        return decorate

    def execute(self, action_name, *args, **kwargs):
        action = self.actions[action_name]

        return action(*args, **kwargs)


manager = Manager()

# %% function for import products from *.csv file


@manager.assign('whs_read')
def read_store(store, filename):
    with open(filename, 'r') as file:
        for row in file.readlines():
            splitted_row = row.replace('\n', '').split(',')
            name = splitted_row[0]
            price = float(splitted_row[1])
            count = int(splitted_row[2])

            store_dict = {
                'product_price': price,
                'product_count': count
                }
            store[name] = store_dict
    return store

# %% function for check items count in warehouse


@manager.assign('whs_check')
def warehouse_checker(product_name, store, operation_history):

    product_info = store.get(product_name)

    message = f"Sprawdzono stan magazynowy przedmiotu {product_name}."

    message_no_item = (f"Sprawdzono stan magazynowy przedmiotu {product_name}"
                       f". Nie ma towaru '{product_name}' w magazynie!")

    if product_info:
        print(store[product_name])
        operation_history.append(message)
    else:
        print(f'Nie ma towaru "{product_name}" w magazynie!')
        operation_history.append(message_no_item)


# %% account balance import function


@manager.assign('acc_read')
def read_account_balance(account_balance_file):
    account_balance_open = open(account_balance_file)
    account_balance_str = account_balance_open.read()
    account_balance = float(account_balance_str)
    return account_balance

# %% account balance export/save function


@manager.assign('acc_write')
def write_account_balance(account_balance, account_balance_file):
    with open(account_balance_file, 'w') as file:
        file.write(f"{account_balance}")

# %% account balance display function


@manager.assign('acc_display')
def display_account_balance(account_balance):
    print(account_balance)


# %% account balance change function

@manager.assign('acc_change')
def change_account_balance(account_balance, operation_history):

    while True:
        try:
            account_balance_change = float(input("Kwota: "))
        except ValueError:
            print("Wprowadzony atrybut nie jest liczb??.")
            continue
        else:
            if account_balance_change == 0:
                print("Wprowadzony atrybut to 0 (zero). "
                      "Brak zmiany na koncie")
                pass
            else:
                break

    user_comment = input("Komentarz do wp??aty/wyp??aty: ")

    if len(user_comment) == 0:
        comment = "Nie wprowadzono komentarza do zmiany salda."
    else:
        comment = f"Komentarz do zmiany: '{user_comment}'."

    if (account_balance + account_balance_change) > 0:
        account_balance += account_balance_change

        msg_deposit_money = (f"Wp??ata kwoty {account_balance_change} "
                             "na konto zako??czona powodzeniem. "
                             f"Twoje saldo wynosi aktualnie {account_balance}."
                             f" {comment}")

        msg_withdraw_money = (f"Wyp??ata kwoty {abs(account_balance_change)} "
                              "z konta zako??czona powodzeniem. Twoje saldo "
                              f"wynosi aktualnie {account_balance}. {comment}")

        if account_balance_change > 0:
            operation_history.append((msg_deposit_money))
        else:
            operation_history.append(msg_withdraw_money)

    else:
        print("Posiadasz za ma??o ??rodk??w na koncie na wyp??acenie takiej "
              f"kwoty. Twoje saldo wynosi {account_balance}.")

        msg_fail = ("Wyp??ata ??rodk??w zako??czona niepowodzeniem. "
                    "Posiadasz za ma??o ??rodk??w na koncie na "
                    f"wyp??acenie kwoty {abs(account_balance_change)}. "
                    f"Twoje saldo wynosi {account_balance}.")
        operation_history.append(msg_fail)

    return account_balance

# %% function for buy items to warehouse


@manager.assign('kupno')
def buy(product_name, store, account_balance, operation_history):

    while True:
        try:
            product_price = float(input("Cena: "))
        except ValueError:
            print("Wprowadzony atrybut nie jest liczb?? dodatni??.")
            continue
        else:
            if product_price <= 0:
                print("Cena produktu musi by?? dodatnia.")
                pass
            else:
                break

    while True:
        try:
            product_count = int(input("Ilo????: "))
        except ValueError:
            print("Wprowadzony atrybut nie jest liczb??.")
            continue
        else:
            if product_count <= 0:
                print("Liczba musi by?? dodatnia.")
                pass
            else:
                break

    product_total_price = (product_price * product_count)

    message_fail = ("Niewystarczaj??ce ??rodki na koncie. Zakup towaru nie "
                    "mo??e by?? zrealziowany.")

    message_buy = (f"Zakupiono {product_count} sztuk produktu "
                   f"{product_name}, kt??rego cena za sztuk?? wynosi "
                   f"{product_price}. "
                   f"Ca??kowita kwota zakupu wynosi {product_total_price}.")

    if product_total_price > account_balance:
        print("Posiadasz za ma??o ??rodk??w na koncie na zakup takiej ilo??ci "
              f"towaru za {product_total_price}. Twoje saldo wynosi "
              f"{account_balance}.")
        operation_history.append(message_fail)
    else:
        operation_history.append(message_buy)
        account_balance -= product_total_price

        if product_name in store.keys():
            store[product_name]['product_price'] = product_price
            store[product_name]['product_count'] += product_count
        else:
            store[product_name] = {'product_price': product_price,
                                   'product_count': product_count}

    return(account_balance)

# %% function for sell items from store


@manager.assign('sprzedaz')
def sell(product_name, store, account_balance, operation_history):

    message_fail = (f"Niewystarczaj??ca ilo???? produktu {product_name}."
                    " Sprzeda?? towaru nie mo??e zasta?? zrealizowana.")

    if (product_name in store.keys() and
            store[product_name]['product_count'] > 0):
        while True:
            try:
                product_count = int(input("Liczba sprzedawanych "
                                          "przedmiot??w: "))
            except ValueError:
                print("Wprowadzony atrybut nie jest liczb??.")
                continue
            else:
                if product_count <= 0:
                    print("Liczba musi by?? dodatnia.")
                    pass
                elif product_count > store[product_name]['product_count']:
                    print("Na stanie znajduje si?? tylko "
                          f"{store[product_name]['product_count']} sztuk tego "
                          f"produktu {product_name}. Podaj inn?? liczb?? "
                          "sprzedawanych sztuk.")
                    operation_history.append(message_fail)
                    pass
                else:
                    break

        total_purchase = store[product_name]['product_price'] * product_count

        message_sell = (f"Sprzedano {product_count} sztuk produktu "
                        f"{product_name}, kt??rego cena za sztuk?? wynosi "
                        f"{store[product_name]['product_price']}. Ca??kowita "
                        f"kwota sprzeda??y wynosi {total_purchase}.")

        if product_count <= store[product_name]['product_count']:
            store[product_name]['product_count'] -= product_count
            account_balance += total_purchase
            operation_history.append(message_sell)

    elif (product_name in store.keys() and
          store[product_name]['product_count'] == 0):
        print("Artyku?? aktualnie niedost??pny.")
        operation_history.append(message_fail)
    else:
        print("Brak artyku??u o takiej nazwie.")

    return(account_balance)

# %% function for export/save products to *.csv file


@manager.assign('whs_write')
def write_store(store, filename):
    with open(filename, 'w') as file:
        for product in store.keys():
            product_name = product
            product_price = store[product]['product_price']
            product_count = store[product]['product_count']
            file.write(f"{product_name},{product_price},{product_count}\n")

# %% function for generating reports for current program working session


@manager.assign('raport')
def generate_report(operation_history):
    msg_report = "Wygenerowano raport."
    operation_history.append(msg_report)
    print("_" * 5 + "\nRaport\n")

    for operation in operation_history:
        print(operation + "\n")

    print("_" * 5 + "\nKoniec raportu\n")
