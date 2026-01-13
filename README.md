# Stock Monte Carlo Forecaster

A quantitative tool for simulating S&P 500 (VFV.TO) price trajectories using Geometric Brownian Motion (GBM).

## The Story Behind This Project

During the Fall 2025 semester at UTSC, I found myself immersed in the theoretical frameworks of **MGEB11 (Quantitative Methods in Economics)** and **STAB53 (Introduction to Applied Statistics)**. Concepts like confidence intervals, quantiles, and stochastic processes were no longer just textbook formulas—they felt like tools that could decode market uncertainty.

In the world of finance, using AI to predict exact stock prices is often seen as "pseudiscience." I was drawn to the **Monte Carlo Method** because it doesn't offer a single "guess," but rather a probabilistic range of outcomes. I realized that by calculating the **5th and 95th quantiles** and visualizing the **expected mean** with shaded confidence regions, I could create a clear, statistically-grounded forecast range.

To bring this to life, I revisited the Python fundamentals I learned in **CSCA08 (Introduction to Computer Science)** during my first semester. I developed the core back-end logic and then collaborated with **Gemini** to bridge the gap into front-end engineering. Through this partnership, I learned to navigate Streamlit and Plotly, eventually building the framework for the interactive app you see today.

## Technical Implementation

### Core Methodology
The simulation utilizes **Geometric Brownian Motion (GBM)**:
$$dS_t = \mu S_t dt + \sigma S_t dW_t$$

By extracting historical drift ($\mu$) and volatility ($\sigma$) from real-time YFinance data, the model generates 500+ random walks to quantify uncertainty rather than predicting a deterministic price.

### Key Functionalities
- **Live Data Pipeline:** Handles complex multi-index structures from `yfinance`.
- **Dynamic Analysis:** Interactive return density plots with magnetic spikelines for granular inspection of "Fat Tails."
- **Risk Metrics:** Real-time calculation of Value-at-Risk (VaR) and probabilistic forecasting horizons.
- **Macro Integration:** A 'Macro Bias' slider allows for stress-testing historical data against forward-looking economic expectations.

## Tech Stack
- **Languages:** Python (NumPy, Pandas, SciPy)
- **Frameworks:** Streamlit, Plotly
- **Infrastructure:** Streamlit Cloud

---
**Author:** XXStvXX (UTSC 2028)
*Major in Statistics & Economics | Minor in English-Chinese Translation*
