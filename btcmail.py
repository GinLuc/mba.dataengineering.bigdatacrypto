
from requests import Session
from datetime import datetime
import json
import os
import smtplib
import smtplib
from email.mime.text import MIMEText

import database as db 

limitValue = 130000
sender = 'dataengineering@faculdadeimpacta.com'
receivers = ['exampleclient@outlook.com', 'joanadarc@hotmail.com', 'johnmarson@gmail.com']
COINMARKETCAP_API_KEY = 'a8a60589-ca4f-4e8a-8a7f-16b9af8f3e55'
SMTP_SERVER = '0.0.0.0'
DATABASE_PASSWORD = "FaculdadeImpacta@2023"
LIMIT_VALUE = 130000.00

# Prints log
def print_log(text):
    print(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")) + ' - ' + text)

def getBitcoinQuotes():

    print_log('Connecting to cryto database...')
    connection = db.get_connection(DATABASE_PASSWORD)
    low_price = db.getDatabaseQuotes(connection, 
                                     query="SELECT LOW_VALUE FROM QUOTES WHERE CRYPTO_ID='BTC' ORDER BY HISTORICAL_DATE DESC FETCH FIRST ROWS ONLY")[0][0]

    print_log("Preço do Bitcoin: US$ {0}".format(low_price))

    if(low_price < LIMIT_VALUE):
        print_log("Bitcoin é menor que US$ {0}".format(LIMIT_VALUE))
        try:
            smtpServer = SMTP_SERVER +':1025'
            smtpObj = smtplib.SMTP(smtpServer)
            for receiver in receivers:
                message = MIMEText("""
                    Ola,

                    A seu pedido, viemos comunicar que o menor valor do BitCoin atual (US$ {0}) esta menor que o limite estipulado 
                    (US$ {1}).

                    Caso tenha alguma duvida, favor entrar em contato com nossos especialistas.

                    Boas Transacoes,
                    Equipe Data Engineering.
                    """.format(str(low_price), str(LIMIT_VALUE)))
                message['Subject'] = "Valor do BitCoin"
                message['From'] = 'dataengineering@faculdadeimpacta.com'
                message['To'] = receiver
                smtpObj.sendmail(sender, receiver, message.as_string())
                print_log("E-mail enviado para o destinatário {0}".format(receiver))
        except Exception as e:
            print_log("Erro ao enviar o e-mail: {0}".format(e))
    else:
        print_log("Bitcoin é maior ou igual a US$ "+str(LIMIT_VALUE))
        print_log("E-mail não enviado")


if __name__=='__main__':
    getBitcoinQuotes()