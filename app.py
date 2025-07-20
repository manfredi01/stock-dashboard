# app.ny

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("Weekly Stock Report Dashboard")

# --- Sidebar ---
st.sidebar.header("Configuration")
tickers = st.sidebar.multiselect("Choose stocks", ["AAPL", "MSFT", "GOOGL", "AMZN", "META"], default=["AAPL", "MSFT"])
start_date = st.sidebar.date_input("Start Date", pd.to_datetime("2025-01-01"))
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))

if tickers:
  # --- Load data ---
  data = yf.download(tickers, start=start_date, end=end_date)["Close"]
  returns = data.pct_change().dropna()

  st.subheader("1. Raw Prices")
  st.line_chart(data)

  st.subheader("2. Metrics Table")
  volatility = returns.std()
  mean_returns = returns.mean()
  sharpe = mean_returns/volatility

  metrics = pd.DataFrame({
      "Mean Return": mean_returns,
      "Volatility": volatility,
      "Sharpe Ratio": sharpe
  })

  st.dataframe(metrics.style.format("{:.4f}"))

  # --- Correlation Heatmap ---
  st.subheader("3. Correlation Heatmap")
  fig1, ax1 = plt.subplots()
  sns.heatmap(returns.corr(), annot=True, cmap="coolwarm", ax=ax1)
  st.pyplot(fig1)

  # --- Weekday Returns ---
  st.subheader("4. Average Returns by Weekday")
  returns["Weekday"] = returns.index.day_name()
  weekday_avg = returns.groupby("Weekday").mean()
  weekday_avg = weekday_avg.loc[["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]]

  fig2, ax2 = plt.subplots()
  weekday_avg.plot(kind="bar", ax=ax2)
  st.pyplot(fig2)

 # --- Download CSV ---
  st.subheader("5. Download Data")
  st.download_button("Download Returns CSV", data=returns.to_csv(), file_name="returns.csv", mime="text/csv")

else:
  st.warning("Please select at least one stock.")
