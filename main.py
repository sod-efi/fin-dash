import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests

def get_market_cap_data(stock, api_key):
    url = f"https://financialmodelingprep.com/api/v3/enterprise-values/{stock}?limit=40&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if data:
        return data
    else:
        raise ValueError(f"No data found for {stock}")

def get_total_assets_data(stock, api_key):
    url = f"https://financialmodelingprep.com/api/v3/balance-sheet-statement-as-reported/{stock}?limit=10&apikey={api_key}"
    response = requests.get(url)
    data = response.json()
    if data:
        return data
    else:
        raise ValueError(f"No data found for {stock}")

def get_market_cap_to_assets_ratio(stock, api_key):
    market_cap_data = get_market_cap_data(stock, api_key)
    total_assets_data = get_total_assets_data(stock, api_key)

    market_cap_df = pd.DataFrame(market_cap_data, columns=["date", "marketCapitalization"])
    total_assets_df = pd.DataFrame(total_assets_data, columns=["date", "assets"])

    data = market_cap_df.merge(total_assets_df, on="date")
    data["date"] = pd.to_datetime(data["date"])
    data["ratio"] = data["marketCapitalization"] / data["assets"]

    return data

st.title("Stock Dashboard")
st.write("Enter a list of up to 100 stock symbols separated by commas:")

stocks_input = st.text_input("Stock symbols (e.g., AAPL,GOOG,MSFT)")
stocks = [stock.strip().upper() for stock in stocks_input.split(",")]

start_date = st.date_input("Start date", value=pd.to_datetime("2010-01-01"))
end_date = st.date_input("End date", value=pd.to_datetime("today"))


api_key = st.text_input("Enter your API Key:", type="password")

if st.button("Show Dashboard"):
    for stock in stocks:
        st.subheader(f"{stock} Market Cap / Total Assets Ratio")
        try:
            mc_ta_ratio = get_market_cap_to_assets_ratio(stock, api_key)
            mc_ta_ratio = mc_ta_ratio[(mc_ta_ratio["date"] >= pd.to_datetime(start_date)) & (mc_ta_ratio["date"] <= pd.to_datetime(end_date))]

            fig, ax = plt.subplots()
            ax.plot(mc_ta_ratio["date"], mc_ta_ratio["ratio"], label=stock)
            ax.set(xlabel="Date", ylabel="Market Cap / Total Assets Ratio")
            ax.legend()
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Error fetching data for {stock}: {str(e)}")
