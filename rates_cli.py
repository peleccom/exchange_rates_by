import argparse
from rates import MyfinClient
                    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Получить актуальный курс валют')
    parser.add_argument('currency',
        help='currency code', choices=['usd', 'eur', 'rub100'])
    parser.add_argument('--bank',
        help='filter by bank')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('--sell', action='store_true', help="Показывать только покупку")
    group.add_argument('--buy', action='store_true', help="Показывать только продажу")

    args = parser.parse_args()
    currency = args.currency
    bank = args.bank
    only_sell = args.sell
    only_buy = args.buy
    
    rows = MyfinClient().get_rates(currency)
    for row in rows:
        bank_name = row['name']
        rate = row['rate']
        
        show_components = []

        if not bank or bank == bank_name:
            if not bank:
                show_components.append(bank_name)
            if not only_buy and not only_sell:
                show_components.append(rate.buy)
                show_components.append(rate.sell)
            elif only_buy:
                show_components.append(rate.buy)
            elif only_sell:
                show_components.append(rate.sell)
            print(*show_components)
