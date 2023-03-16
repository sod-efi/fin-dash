import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

def main():
    symbols = symbol_list.strip().split('\n')
    data = yf.download(symbols, start='2010-01-01', end='2022-01-01')
    market_cap = data['Close'].resample('Q').last() * data['Shares Outstanding'].resample('Q').last()
    total_assets = data['Total Assets'].resample('Q').last()
    ratio = market_cap / total_assets

    for symbol in symbols:
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ratio.index, y=ratio[symbol], name=symbol))
        fig.update_layout(title=f'{symbol} Market Cap/Total Assets Ratio', xaxis_title='Quarter', yaxis_title='Market Cap/Total Assets Ratio')
        st.plotly_chart(fig)

st.set_page_config(page_title='Stock Ratios Dashboard')
st.title('Stock Ratios Dashboard')
symbol_list = st.sidebar.text_area('Enter stock symbols (one per line)', height=500)
if symbol_list:
    main()
else:
    st.warning('Please enter at least one stock symbol.')

    
    
