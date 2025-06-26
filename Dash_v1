# fo_dashboard/app.py

import streamlit as st
import pandas as pd
import json
import os
from utils.dhan_api import get_ltp, fetch_ticker_data
from utils.auth import authenticate_user, get_user_role, get_pending_users, approve_user
from utils.trade_utils import load_user_trades, save_user_trades, analyze_trades, calculate_mtm
from utils.alerts import load_alerts, save_alerts, check_alerts, add_alert

# -------------------- SETTINGS --------------------
st.set_page_config(page_title="F&O Trade Tracker", layout="wide")

# -------------------- TICKER ----------------------
nifty_symbols = [
    "NIFTY24JUNFUT", "RELIANCE24JUNFUT", "INFY24JUNFUT",
    "HDFCBANK24JUNFUT", "TCS24JUNFUT", "ICICIBANK24JUNFUT"
]

def display_ticker():
    data = fetch_ticker_data(nifty_symbols)
    items = " | ".join([f"{sym}: ₹{data[sym]}" for sym in data])
    st.markdown(f"""
        <marquee behavior="scroll" direction="left" scrollamount="4"
                 style="color: white; background: black; padding: 8px; font-size: 18px;">
            {items}
        </marquee>
    """, unsafe_allow_html=True)

# -------------------- MAIN APP --------------------

def main():
    display_ticker()

    user_email = authenticate_user()
    if not user_email:
        st.warning("Please login with Google to access the dashboard.")
        return

    role = get_user_role(user_email)
    if role == "pending":
        st.info("Your request is under review. Please wait for admin approval.")
        return
    elif role == "admin":
        admin_panel()

    st.title("📊 F&O Trade Tracker")
    
    st.sidebar.header("Upload Trades")
    uploaded_file = st.sidebar.file_uploader("Upload CSV", type=["csv"])

    trades = load_user_trades(user_email)

    if uploaded_file:
        new_trades = pd.read_csv(uploaded_file)
        trades = pd.concat([trades, new_trades], ignore_index=True)
        save_user_trades(user_email, trades)

    if not trades.empty:
        mtm_df = calculate_mtm(trades)
        st.subheader("📋 Your Trades + MTM")
        st.dataframe(mtm_df, use_container_width=True)

        st.subheader("📈 Performance Summary")
        stats = analyze_trades(trades)
        for k, v in stats.items():
            st.metric(label=k, value=v)

    # Alerts & Signals
    st.subheader("📡 Signals & Price Alerts")
    alerts = load_alerts(user_email)
    updated_alerts = check_alerts(alerts)
    st.dataframe(pd.DataFrame(updated_alerts))

    with st.expander("➕ Add New Alert"):
        col1, col2, col3 = st.columns(3)
        with col1:
            symbol = st.text_input("Symbol")
        with col2:
            trigger = st.number_input("Trigger Price")
        with col3:
            note = st.text_input("Note")
        if st.button("Add Alert"):
            add_alert(user_email, symbol, trigger, note)
            st.success("Alert added!")

# -------------------- ADMIN PANEL --------------------
def admin_panel():
    st.sidebar.subheader("🛠️ Admin Panel")
    if st.sidebar.button("Review User Requests"):
        pending = get_pending_users()
        for email in pending:
            col1, col2 = st.columns([3, 1])
            col1.write(email)
            if col2.button("Approve", key=email):
                approve_user(email)
                st.success(f"Approved {email}")

# -------------------- START APP --------------------
if __name__ == "__main__":
    main()
