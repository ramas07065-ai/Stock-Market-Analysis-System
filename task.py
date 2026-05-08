import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# ==========================================
# MEMBER 2 & 3: YOUR COMPLETED TASKS
# ==========================================

def clean_stock_data(raw_data):
    """ MEMBER 2: Data Processing """
    df = raw_data.reset_index()
    # Keep only required columns
    df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
    # Fix 1: Round numbers to 2 decimals
    df = df.round(2)
    # Fix 2: Clean the date format (Removes the 00:00:00 mess)
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    return df

def create_stock_chart(df, symbol, company_name):
    """ MEMBER 3: Visualization """
    fig = go.Figure()
    # Added 'markers' to make the chart look more professional
    fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], mode='lines+markers', name='Close Price'))
    fig.update_layout(
        title=f"{company_name} ({symbol}) Price Trend",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

# ==========================================
# APP UI & EXECUTION
# ==========================================

st.set_page_config(page_title="Stock Market Analysis System", layout="wide")
st.title("ð Stock Market Analysis System")
st.markdown("Developed for **Dr. Khalaf's** BIS Project")

symbol = st.text_input("Enter Stock Symbol:", "AAPL").upper()
time_period = st.selectbox("Select Time Period:", ["7 Days", "1 Month"])
days = 7 if time_period == "7 Days" else 30

if symbol:
    try:
        ticker = yf.Ticker(symbol)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        hist = ticker.history(start=start_date, end=end_date)

        if not hist.empty:
            # --- APPLYING YOUR CLEANING (Member 2) ---
            cleaned_data = clean_stock_data(hist)
            
            info = ticker.info
            company_name = info.get('longName', symbol)
            current_price = cleaned_data['Close'].iloc[-1]
            
            st.metric(label=f"Company: {company_name}", value=f"{current_price:.2f} USD")
            
            # --- APPLYING YOUR CHART (Member 3) ---
            create_stock_chart(cleaned_data, symbol, company_name)

            st.subheader(f"Historical Data ({time_period})")
            # Displaying your clean table
            st.dataframe(cleaned_data.sort_values(by='Date', ascending=False), use_container_width=True)
        else:
            st.error("No data found for this symbol.")
    except Exception as e:
        st.error(f"Error: {e}")
