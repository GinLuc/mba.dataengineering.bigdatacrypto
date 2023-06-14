#This example uses Python 2.7 and the python-request library.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import datetime

COINMARKETCAP_API_KEY='a8a60589-ca4f-4e8a-8a7f-16b9af8f3e55'
coins = ['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'DOGE', 'SOL', 'MATIC', 'LTC', 'ETC']
ALPHAVANTAGE_API_KEY="LLLP6J45T2JASZWI"

def execute_sample():
  url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
  parameters = {
    'start':'1',
    'limit':'5000',
    'convert':'USD'
  }
  headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
  }

  session = Session()
  session.headers.update(headers)

  try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    with open("data/coinmarketcap_api_results.json", 'w') as file:
      json.dump(data, file)
      print(data)
  except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)

def getImageCoin():
    coinsConcatenated = ','.join(coins)
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/info' # Coinmarketcap API url
    parameters = { 
        'symbol': coinsConcatenated,
        'aux': 'logo'
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY
    }

    session = Session()
    session.headers.update(headers)

    print('Connecting to api coinmarketcap...')
    response = session.get(url, params=parameters)

    info = json.loads(response.text)
    if info['status']['error_code'] != 0:
        print(info['status']['error_message'])
        return []
    return info['data']


# Getting quotes
def getQuotes(coin):
    url = 'https://www.alphavantage.co/query'
    
    parameters = { 
        'function': 'DIGITAL_CURRENCY_DAILY',
        'symbol': coin,
        'market': 'USD',
        'apikey': ALPHAVANTAGE_API_KEY
    }

    headers = {
        'Accept': 'application/json'
    }

    session = Session()
    session.headers.update(headers)

    print('Connecting to api alphavantage ('+coin+')...')
    response = session.get(url, params=parameters)

    info = json.loads(response.text)
    if 'Error Message' in info:
        print(info['Error Message'])
        return []
    return info


if __name__=='__main__':
  info = getQuotes()
  with open("data/info_alphavantage_api_results.json", 'w') as file:
    json.dump(info, file)
    print(info)
  