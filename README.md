# 🏦 GMF Portfolio Optimization Capstone

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3110/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📊 Project Overview
This project transforms a financial forecasting model into a production-grade portfolio management tool for **Guide Me in Finance (GMF) Investments**. It utilizes classical statistics (ARIMA) and deep learning (LSTM) to predict asset trends and optimizes portfolio allocation using Modern Portfolio Theory (MPT).

## 💼 Business Problem
Financial advisors often rely on static allocation strategies that fail to adapt to market volatility. GMF Investments requires a dynamic, data-driven system to maximize client returns while strictly managing risk across diverse asset classes (High-growth stocks, Bonds, and Market ETFs).

## 🚀 Solution Overview
- **Advanced Forecasting:** Hybrid approach using ARIMA for linear trends and LSTM for complex, non-linear patterns.
- **Portfolio Optimization:** Implementation of the Efficient Frontier to find the optimal risk-return balance.
- **Interactive Dashboard:** A Streamlit-based interface for real-time simulation and "what-if" analysis.
- **Explainable AI:** Integration of SHAP to provide transparency into model predictions, building trust with finance stakeholders.

## 📈 Key Results
- **Dynamic Allocation:** Responsive weighting that outperforms static 60/40 benchmarks in backtesting.
- **Reliability:** Built with modular code, comprehensive type hinting, and unit testing.
- **Transparency:** Clear visualization of risk-return trade-offs and model drivers.

## 🛠️ Quick Start

### Prerequisites
- Python 3.11+
- Git

### Installation
```bash
# Clone the repository
git clone https://github.com/your-username/gmf-portfolio-optimization.git
cd gmf-portfolio-optimization

# Set up virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Dashboard
```bash
# Set PYTHONPATH to the project root
$env:PYTHONPATH = "."

# Launch Streamlit
streamlit run dashboard/app.py
```

## 📂 Project Structure
```text
├── dashboard/          # Streamlit dashboard application
├── src/                # Core logic (Ingestion, Modeling)
│   ├── data_processing.py
│   ├── models.py
│   └── main.py
├── tests/              # Unit and integration tests
├── data/               # Local data storage (ignored by git)
│   ├── raw/
│   └── processed/
├── .github/            # CI/CD Workflows
└── README.md
```

## 🔮 Future Improvements
- **Real-time API Integration:** Connect to live Bloomberg or Reuters feeds.
- **Multi-Asset Expansion:** Support for crypto and commodity asset classes.
- **Advanced RL:** Implementing Reinforcement Learning for automated trade execution.

## 👤 Author
**Tekalegn Mekonen**
- [LinkedIn](www.linkedin.com/in/tekalegn-mekonen-456b662a7)
- [GitHub](https://github.com/tekamek123)
