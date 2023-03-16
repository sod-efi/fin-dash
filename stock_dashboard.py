import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

def get_market_cap_to_assets_ratio(stock, start_date, end_date):
    df = yf.download(stock, start=start_date, end=end_date, progress=False, auto_adjust=True)
     if not hasattr(df.index, 'tz_localize'):
        df.index = pd.to_datetime(df.index, utc=True)
    df['Market Cap'] = df['Close'] * df['Volume']
    df['Total Assets'] = df['Market Cap'] / 1.5  # You need to replace this with a real API to fetch the total assets
    df['MC/TA Ratio'] = df['Market Cap'] / df['Total Assets']
    df = df.resample('Q').mean()
    return df['MC/TA Ratio']

st.title("Stock Dashboard: Market Cap / Total Assets Ratio")

stock_input = st.text_area("Enter a list of up to 100 stock symbols separated by commas:", max_chars=1000)
stocks = [s.strip() for s in stock_input.split(',') if s.strip()]

start_date = st.date_input("Start date", value=pd.to_datetime("2010-01-01"))
end_date = st.date_input("End date", value=pd.to_datetime("today"))

if st.button("Show Dashboard"):
    if len(stocks) > 100:
        st.warning("Please enter a maximum of 100 stock symbols.")
    else:
        for stock in stocks:
            st.subheader(f"{stock} Market Cap / Total Assets Ratio")
            try:
                mc_ta_ratio = get_market_cap_to_assets_ratio(stock, start_date, end_date)
                plt.figure(figsize=(10, 5))
                plt.plot(mc_ta_ratio)
                plt.xlabel("Date")
                plt.ylabel("MC/TA Ratio")
                st.pyplot(plt)
            except Exception as e:
                st.error(f"Error fetching data for {stock}: {e}")
