import os
import streamlit as st
import pandas_datareader as pdr
import pandas as pd
import matplotlib.pyplot as plt
import requests

def get_financial_data(stock, api_key):
    url = f"https://financialmodelingprep.com/api/v3/profile/{stock}?apikey={d24086a7252e0ce8946a897be9845c8e}"
    response = requests.get(url)
    data = response.json()
    if data:
        return data[0]['mktCap'], data[0]['totalAssets']
    else:
        raise ValueError(f"No data found for {stock}")

def get_market_cap_to_assets_ratio(stock, start_date, end_date, api_key):
    market_cap, total_assets = get_financial_data(stock, api_key)
    df = pdr.get_data_yahoo(stock, start=start_date, end=end_date)
    df['Market Cap'] = market_cap
    df['Total Assets'] = total_assets
    df['MC/TA Ratio'] = df['Market Cap'] / df['Total Assets']
    df = df.resample('Q').mean()
    return df['MC/TA Ratio']

st.title("Stock Market Cap / Total Assets Ratio Dashboard")

api_key = st.text_input("Enter your Financial Modeling Prep API Key:", type="password")

stocks = st.text_input("Enter up to 100 stock symbols separated by commas:", "AAPL,MSFT,GOOG")
stocks = stocks.split(',')

start_date = st.date_input("Start Date:", value=pd.to_datetime('2020-01-01'))
end_date = st.date_input("End Date:", value=pd.to_datetime('2021-12-31'))

if st.button("Show Dashboard"):
    for stock in stocks:
        st.subheader(f"{stock} Market Cap / Total Assets Ratio")
        try:
            mc_ta_ratio = get_market_cap_to_assets_ratio(stock, start_date, end_date, api_key)
            plt.figure(figsize=(12, 6))
            plt.plot(mc_ta_ratio)
            plt.xlabel("Date")
            plt.ylabel("MC/TA Ratio")
            plt.title(f"{stock} Market Cap / Total Assets Ratio")
            st.pyplot(plt)
        except Exception as e:
            st.error(f"Error fetching data for {stock}: {e}")
