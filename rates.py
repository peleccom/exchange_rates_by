import re
import json 
import datetime
from decimal import Decimal
import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent


AVAILAIBLE_CURRENCIES = [
    'usd',
    'eur',
    'rub100',
]

CITY = 'minsk'

class ExchangeRate:
    def __init__(self, buy, sell):
        self.buy = buy
        self.sell = sell

class MyfinClient:
    
    def get_rates(self, currency, bank=None):
        if currency not in AVAILAIBLE_CURRENCIES:
            raise ValueError(f'invalid currency code {currency}')
            
        result = []        
        url = f'https://myfin.by/currency/{CITY}'
        headers = {'User-Agent': generate_user_agent(device_type="desktop", os=('mac', 'linux'))}        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        
        best_rates_table = soup.body.find('div', class_='best-rates').find('table')
        
        best_rates_rows = best_rates_table.find('tbody').find_all('tr')
        nbrb_bank_name = 'НБ РБ'
        if not bank or bank == nbrb_bank_name:
            for best_rates_row in best_rates_rows:
                cells = best_rates_row.find_all('td')
                best_rates_currency = cells[0].find('a', href=True)['href'].replace('/currency/','')
                if (currency == 'rub100' and best_rates_currency== 'rub') or (best_rates_currency == currency):
                    result.append(dict(name=nbrb_bank_name, rate=ExchangeRate(Decimal(cells[3].text), Decimal(0))))
        rates_table = soup.body.find('div', class_='page_currency').find('table', class_ = 'rates-table-sort')
        
        cols = rates_table.find('thead').find_all('th', class_='cur-name')
        currencies = []
        for col in cols:
            currencies.append(col.text)
        
        bank_lines = rates_table.find_all('tr', class_='tr-tb')
        col_index = currencies.index(currency)
        if col_index == -1:
           raise ValueError(f'invalid currency code {currency}')

        for bank_line in bank_lines:
            cells = bank_line.find_all('td')
            bank_name = cells[0].text.strip()
            if bank and bank != bank_name:
                continue
            buy = Decimal(cells[1 + col_index * 2].text)
            sell = Decimal(cells[1 + col_index * 2 + 1].text)
            result.append(dict(name=bank_name, rate=ExchangeRate(buy, sell)))
        return result
    
class TutByFinanceClient:

    def normalize_rate(self, items):
        denomination_date = datetime.date(2016, 6, 30)
        for item in items:
            if item['date'] <= denomination_date and item['value'] > 5:
                item['value'] = item['value'] / 10000
        return items

    def hist(self, currency):
        if currency not in AVAILAIBLE_CURRENCIES:
            raise ValueError(f'invalid currency code {currency}')
        cur = currency
        if cur == 'rub100':
            cur = 'rub'
        response = requests.get(f'https://finance.tut.by/informer/amstock/{cur}.js')
        response.raise_for_status()
        response_text = response.text
        mre = re.search(r'\=(\[.*\])', response_text)
        if not mre:
            raise ValueError('wong response')
        json_str = mre.group(1)
        items = json.loads(json_str)

        for item in items:
            date_str = item['date']
            item['date'] = datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
            item['value'] = Decimal(item['value'])

        items = self.normalize_rate(items)
        return items
   