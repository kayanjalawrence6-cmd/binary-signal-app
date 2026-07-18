import pandas_ta as ta
import streamlit as st
import yfinance as yf

# 1. Design the Web Screen Layout
st.title("Binary Signal Scanner")
st.write("Select a market pair to scan for instant short-term signals.")

# Dropdown menu for pairs
selected_pair = st.selectbox(
    "Choose Currency Pair:", ["EURUSD=X", "GBPUSD=X", "AUDUSD=X"]
)

# The "Get Signal" Button
if st.button("GET SIGNAL", type="primary"):
    st.write("Analyzing market structure...")

    try:
        # 2. Fetch Live Market Data (Last 50 candles, 5-minute interval)
        data = yf.download(tickers=selected_pair, period="1d", interval="5m")

        if data.empty:
            st.error("Could not fetch data. Try again.")
        else:
            # 3. Compute Technical Analysis
            rsi = ta.rsi(data["Close"], length=14).iloc[-1]
            ema_20 = ta.ema(data["Close"], length=20).iloc[-1]
            current_price = data["Close"].iloc[-1]

            # 4. Generate Signal Output
            if current_price > ema_20 and rsi < 35:
                st.success("🎯 CALL (Buy) - 5 Min Expiry")
            elif current_price < ema_20 and rsi > 65:
                st.error("🎯 PUT (Sell) - 5 Min Expiry")
            else:
                st.warning("⏳ NO SIGNAL - Wait for better market alignment")

    except Exception as e:
        st.error(f"Error processing data: {e}")
      
