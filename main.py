from requests import Session
from datetime import datetime
import time
import os
import oracledb
import json
import getpass

import database as db
import coinsquotesapi as api


coins = ['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'DOGE', 'SOL', 'MATIC', 'LTC', 'ETC']


password = getpass.getpass("Enter database password: ")


# Getting historical quotes
def getHistoricalQuotes():
    connection = db.get_connection(password)
    count = 1
    try:
        for c in coins:
            info = api.getQuotes(c)
            if 'Meta Data' in info:
                name = info['Meta Data']['3. Digital Currency Name']
                symbol = info['Meta Data']['2. Digital Currency Code']
                db.insertCoinDb(connection, symbol, name, '', '')
                for i in info['Time Series (Digital Currency Daily)']:
                    print("Inserting " + i + " quotes to " + name)
                    open = info['Time Series (Digital Currency Daily)'][i]['1b. open (USD)']
                    close = info['Time Series (Digital Currency Daily)'][i]['4b. close (USD)']
                    high = info['Time Series (Digital Currency Daily)'][i]['2b. high (USD)']
                    low = info['Time Series (Digital Currency Daily)'][i]['3b. low (USD)']
                    volume = info['Time Series (Digital Currency Daily)'][i]['5. volume']
                    marketCap = info['Time Series (Digital Currency Daily)'][i]['6. market cap (USD)']
                    db.insertQuoteDb(connection, i, symbol, open, close, high, low, volume, marketCap)
            if((count%5) == 0): # 5 API requests per minute and 500 requests per day
                print("Waiting...")
                time.sleep(70) #Waits
            count += 1
        print("Updating logo's coins..")
        images = api.getImageCoin()
        db.saveImageUrlDb(connection, images)
        connection.commit()
    except Exception as e:
        print("Erro! {0}".format(e))
        connection.rollback()
    connection.close()

if __name__=='__main__':
    getHistoricalQuotes()