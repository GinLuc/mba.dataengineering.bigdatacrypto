import streamlit as st
import pandas as pd 

import database as db
import coinsquotesapi as api
from candlestick import get_candlestick_plot


coins = ['BTC', 'ETH', 'BNB', 'XRP', 'ADA', 'DOGE', 'SOL', 'MATIC', 'LTC', 'ETC']
crypto_columns = ['ID', 'HISTORICAL_DATE', 'CRYPTO_ID', 'OPEN_VALUE', 'CLOSE_VALUE', 'HIGH_VALUE', 
           'LOW_VALUE', 'VOLUME', 'MARKET_CAP', 'CREATION_DATE']
DATABASE_PASSWORD = "FaculdadeImpacta@2023"


st.title('Crypto Price App Dashboard')
st.markdown("""
Visualize aqui o histórico das principais criptomoedas da plataforma **CoinMarketCap**!
""")
            

#---------------------------------#
# Page layout (continued)
## Divide page to 3 columns (col1 = sidebar, col2 and col3 = page contents)
col1 = st.sidebar
col2, col3 = st.columns((2,1))

#---------------------------------#
# Sidebar + Main panel
col1.header('Opções de entrada')

## Sidebar - Currency price unit
currency_price_unit = col1.selectbox('Selecione aqui o tipo de criptomoeda', coins)


# Web scraping of CoinMarketCap data
@st.cache
def load_data():

    connection = db.get_connection(DATABASE_PASSWORD)
    results = db.getDatabaseQuotes(connection)

    data = pd.DataFrame(columns=crypto_columns)

    data['ID'] = [result[0] for result in results]
    data['HISTORICAL_DATE'] = [result[1] for result in results]
    data['CRYPTO_ID'] = [result[2] for result in results]
    data['OPEN_VALUE'] = [result[3] for result in results]
    data['CLOSE_VALUE'] = [result[4] for result in results]
    data['HIGH_VALUE'] = [result[5] for result in results]
    data['LOW_VALUE'] = [result[6] for result in results]
    data['VOLUME'] = [result[7] for result in results]
    data['MARKET_CAP'] = [result[8] for result in results]
    data['CREATION_DATE'] = [result[9] for result in results]

    return data

df = load_data()


days_to_plot = st.sidebar.slider(
    'Days to Plot', 
    min_value = 1,
    max_value = 300,
    value = 120,
)
ma1 = st.sidebar.number_input(
    'Moving Average #1 Length',
    value = 10,
    min_value = 1,
    max_value = 120,
    step = 1,    
)
ma2 = st.sidebar.number_input(
    'Moving Average #2 Length',
    value = 20,
    min_value = 1,
    max_value = 120,
    step = 1,    
)

# Get the dataframe and add the moving averages
coin_data = df[(df.CRYPTO_ID == currency_price_unit)] 
coin_data[f'{ma1}_ma'] = coin_data['CLOSE_VALUE'].rolling(ma1).mean()
coin_data[f'{ma2}_ma'] = coin_data['CLOSE_VALUE'].rolling(ma2).mean()
coin_data = coin_data[-days_to_plot:]

# Display the plotly chart on the dashboard
st.plotly_chart(
    get_candlestick_plot(coin_data, ma1, ma2, currency_price_unit),
    use_container_width = True,
)


#---------------------------------#
# About
expander_bar = st.expander("About")
expander_bar.markdown("""
* **Implemented by:** Gian Lucca, Juliana Apolo, Lucas, Vitor (MBA Faculdade Impacta Engenharia de Software - Grupo 3)
* **Python libraries:** pandas, streamlit, numpy, matplotlib, seaborn, BeautifulSoup, requests, json, time, oracledb
* **Data source:** [CoinMarketCap](http://coinmarketcap.com) and [AlphaVantage](www.alphavantage.co).
* **Credit:** 
    * Web scraper adapted from the Medium article *[Web Scraping Crypto Prices With Python](https://towardsdatascience.com/web-scraping-crypto-prices-with-python-41072ea5b5bf)* written by [Bryan Feng](https://medium.com/@bryanf). 
    * Candlestick chart adapted from the Medium article *[Easy and Interactive Candlestick Charts in Python](https://medium.com/@dannygrovesn7/using-streamlit-and-plotly-to-create-interactive-candlestick-charts-a2a764ad0d8e)* written by [Danny Groves](https://medium.com/@dannygrovesn7).
""")
