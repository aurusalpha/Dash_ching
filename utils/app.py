# app.py (Streamlit dashboard integration with NSE ticker)

import streamlit as st
from utils.nse_api import fetch_ticker_data

# Define NIFTY 50 stock list
nifty_symbols = [
    "RELIANCE", "INFY", "HDFCBANK", "ICICIBANK", "TCS", "KOTAKBANK", "SBIN", "LT",
    "ITC", "BHARTIARTL", "ASIANPAINT", "MARUTI", "SUNPHARMA", "AXISBANK", "ULTRACEMCO",
    "BAJFINANCE", "NTPC", "HINDUNILVR", "POWERGRID", "INDUSINDBK", "TITAN", "BAJAJFINSV",
    "GRASIM", "TATASTEEL", "ONGC", "JSWSTEEL", "TECHM", "CIPLA", "NESTLEIND", "ADANIENT",
    "ADANIPORTS", "DIVISLAB", "DRREDDY", "BRITANNIA", "HEROMOTOCO", "HCLTECH", "HDFCLIFE",
    "BPCL", "COALINDIA", "EICHERMOT", "HINDALCO", "BAJAJ-AUTO", "SBILIFE", "SHREECEM",
    "APOLLOHOSP", "TATAMOTORS", "UPL", "WIPRO"
]

st.set_page_config(page_title="NIFTY Dashboard", layout="wide")
st.title("📈 NIFTY 50 Price Ticker")

with st.spinner("Fetching live spot prices from NSE..."):
    ltp_data = fetch_ticker_data(nifty_symbols)
    ticker_items = " | ".join([f"{sym}: ₹{ltp_data[sym]}" for sym in ltp_data])

st.markdown(f"""
    <marquee behavior="scroll" direction="left" scrollamount="4"
             style="color: white; background: black; padding: 8px; font-size: 18px;">
        {ticker_items}
    </marquee>
""", unsafe_allow_html=True)

st.success("Tickertape loaded with real-time spot prices.")
