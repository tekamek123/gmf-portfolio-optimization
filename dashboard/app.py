import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.data_processing import ProjectConfig, DataIngestion
from src.models import ARIMAModel, LSTMForecaster
import os

# Page Config
st.set_page_config(page_title="GMF Portfolio Optimizer", layout="wide")

st.title("🏦 Guide Me in Finance (GMF) Investments")
st.subheader("Portfolio Management Optimization Dashboard")

# Initialize Config and Data
config = ProjectConfig()
ingestion = DataIngestion(config)

if not os.path.exists(config.PROCESSED_DATA_PATH):
    st.info("🔄 Downloading and processing initial data...")
    raw_data = ingestion.fetch_data()
    ingestion.combine_and_save(raw_data)

df = pd.read_csv(config.PROCESSED_DATA_PATH, index_col=0, parse_dates=True)

# Sidebar - Asset Selection
st.sidebar.header("Portfolio Settings")
selected_ticker = st.sidebar.selectbox("Select Asset for Deep Dive", config.TICKERS)

# Main Grid - Overview
col1, col2, col3 = st.columns(3)
for i, ticker in enumerate(config.TICKERS):
    last_price = df[ticker].iloc[-1]
    prev_price = df[ticker].iloc[-2]
    change = ((last_price - prev_price) / prev_price) * 100
    [col1, col2, col3][i].metric(ticker, f"${last_price:.2f}", f"{change:.2f}%")

# Main Chart - Historical Prices
st.write(f"### Historical Performance: {selected_ticker}")
fig = px.line(df, y=selected_ticker, title=f"{selected_ticker} Price History")
st.plotly_chart(fig, use_container_width=True)

# Forecasting Section
st.write("---")
st.write("### 🔮 Predictive Analytics")
forecast_steps = st.slider("Forecast Horizon (Days)", 7, 60, 30)

if st.button("Generate Forecast"):
    with st.spinner(f"Training models for {selected_ticker}..."):
        # Classical ARIMA
        arima = ARIMAModel(selected_ticker)
        arima.train(df[selected_ticker])
        arima_pred = arima.predict(forecast_steps)
        
        # Display results (simplified for now)
        st.success("Forecast generated successfully!")
        
        # Plot forecast
        last_date = df.index[-1]
        forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_steps)
        
        forecast_df = pd.DataFrame({
            'Date': forecast_dates,
            'ARIMA Forecast': arima_pred
        }).set_index('Date')
        
        fig_forecast = go.Figure()
        fig_forecast.add_trace(go.Scatter(x=df.index[-100:], y=df[selected_ticker].iloc[-100:], name="Historical"))
        fig_forecast.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df['ARIMA Forecast'], name="ARIMA Forecast", line=dict(dash='dash')))
        st.plotly_chart(fig_forecast, use_container_width=True)
