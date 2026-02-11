import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.data_processing import ProjectConfig, DataIngestion
from src.models import ARIMAModel, LSTMForecaster
from src.explainability import ModelExplainer
import matplotlib.pyplot as plt
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
model_type = st.sidebar.radio("Forecasting Algorithm", ["ARIMA (Statistical)", "LSTM (Deep Learning)"])

# Main Grid - Overview
col1, col2, col3 = st.columns(3)
for i, ticker in enumerate(config.TICKERS):
    last_price = df[ticker].iloc[-1]
    prev_price = df[ticker].iloc[-2]
    change = ((last_price - prev_price) / prev_price) * 100
    [col1, col2, col3][i].metric(ticker, f"${last_price:.2f}", f"{change:.2f}%")

# Main Chart - Historical Prices
st.write(f"### Historical Performance: {selected_ticker}")
fig = px.line(df, y=selected_ticker, title=f"{selected_ticker} Price History", color_discrete_sequence=['#1f77b4'])
st.plotly_chart(fig, width='stretch')

# Forecasting Section
st.write("---")
st.write(f"### 🔮 {model_type} Predictive Analytics")
forecast_steps = st.slider("Forecast Horizon (Days)", 7, 60, 30)

if st.button("Generate Forecast"):
    with st.spinner(f"Training models for {selected_ticker}..."):
        last_date = df.index[-1]
        forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=forecast_steps)
        
        if model_type == "ARIMA (Statistical)":
            arima = ARIMAModel(selected_ticker)
            arima.train(df[selected_ticker])
            preds = arima.predict(forecast_steps)
            label = "ARIMA Forecast"
            
        else:  # LSTM
            lstm = LSTMForecaster(selected_ticker)
            # Use small epochs for quick demo speed in dashboard
            lstm.train(df[selected_ticker], epochs=5)
            
            # Prepare the last window for the recursive forecast
            scaled_input = lstm.scaler.transform(df[selected_ticker].values[-60:].reshape(-1, 1))
            preds = lstm.predict(scaled_input, steps=forecast_steps)
            label = "LSTM Forecast"

            # SHAP Explainability Sub-section
            st.write("#### 🛡️ Model Transparency (SHAP)")
            # Use a sample of the data as background for speed
            sample_data = lstm.scaler.transform(df[selected_ticker].values[-200:].reshape(-1, 1))
            X_background, _ = lstm._prepare_sequences(sample_data)
            X_background = np.reshape(X_background, (X_background.shape[0], X_background.shape[1], 1))
            X_test = X_background[-1:] # Explain the most recent pattern
            
            explainer = ModelExplainer(lstm.model, X_background)
            shap_vals = explainer.explain(X_test)
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.pyplot(explainer.plot_importance(shap_vals, [f"{selected_ticker} Lag"]))
            with col_b:
                st.pyplot(explainer.plot_time_importance(shap_vals, 60))

        # Combined Plot
        forecast_df = pd.DataFrame({'Date': forecast_dates, label: preds}).set_index('Date')
        fig_forecast = go.Figure()
        fig_forecast.add_trace(go.Scatter(x=df.index[-100:], y=df[selected_ticker].iloc[-100:], name="Historical"))
        fig_forecast.add_trace(go.Scatter(x=forecast_df.index, y=forecast_df[label], name=label, line=dict(dash='dash', color='orange')))
        st.plotly_chart(fig_forecast, width='stretch')
        
        st.success(f"{label} generated and explained successfully!")

# Portfolio Optimization Section
st.write("---")
st.write("### ⚖️ Portfolio Optimization (Modern Portfolio Theory)")
st.write("Calculate the optimal asset allocation based on historical risk and returns.")

from src.optimization import PortfolioOptimizer

if st.button("Optimize Portfolio Weights"):
    with st.spinner("Calculating Efficient Frontier..."):
        optimizer = PortfolioOptimizer(df)
        weights = optimizer.optimize_performance()
        ret, vol, sharpe = optimizer.get_performance(weights)
        
        col_w1, col_w2 = st.columns([1, 1])
        
        with col_w1:
            st.write("#### 🎯 Optimal Weights (Max Sharpe)")
            weight_df = pd.DataFrame(list(weights.items()), columns=['Asset', 'Weight'])
            fig_weights = px.pie(weight_df, values='Weight', names='Asset', hole=0.4,
                               title="Recommended Allocation",
                               color_discrete_sequence=px.colors.qualitative.Pastel)
            st.plotly_chart(fig_weights, width='stretch')
            
        with col_w2:
            st.write("#### 📈 Expected Performance")
            st.metric("Expected Annual Return", f"{ret*100:.2f}%")
            st.metric("Annual Volatility (Risk)", f"{vol*100:.2f}%")
            st.metric("Sharpe Ratio", f"{sharpe:.2f}")
            
            st.info("💡 The Sharpe Ratio measures the performance of an investment compared to a risk-free asset, after adjusting for its risk.")

        # Comparison with Equal Weight Portfolio
        st.write("#### ⚖️ Comparison: Strategy vs. Equal Weight")
        equal_weights = {t: 1.0/len(config.TICKERS) for t in config.TICKERS}
        e_ret, e_vol, e_sharpe = optimizer.get_performance(equal_weights)
        
        comparison_data = {
            'Metric': ['Annual Return', 'Volatility', 'Sharpe Ratio'],
            'Optimal (Max Sharpe)': [ret, vol, sharpe],
            'Equal Weight (Benchmark)': [e_ret, e_vol, e_sharpe]
        }
        comp_df = pd.DataFrame(comparison_data)
        
        fig_comp = go.Figure()
        fig_comp.add_trace(go.Bar(x=comp_df['Metric'], y=comp_df['Optimal (Max Sharpe)'], name='Optimal Portfolio'))
        fig_comp.add_trace(go.Bar(x=comp_df['Metric'], y=comp_df['Equal Weight (Benchmark)'], name='Equal Weight'))
        fig_comp.update_layout(title="Optimal vs. Equal Weight Comparison", barmode='group')
        st.plotly_chart(fig_comp, width='stretch')
