#This example uses Python 2.7 and the python-request library.

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

url = 'https://sandbox-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
  'start':'1',
  'limit':'5000',
  'convert':'USD'
}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': 'a8a60589-ca4f-4e8a-8a7f-16b9af8f3e55',
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