# Stock Monte Carlo Forecaster

A Python-based quantitative tool for simulating stock price trajectories using Geometric Brownian Motion (GBM). This application fetches real-time market data to model return distributions and project potential future outcomes via Monte Carlo simulations.

## Technical Implementation

### Core Model
The simulation is built on the Geometric Brownian Motion (GBM) stochastic process:
$$dS_t = \mu S_t dt + \sigma S_t dW_t$$

The engine extracts historical drift ($\mu$) and volatility ($\sigma$) to generate 500+ independent random walks, providing a probabilistic outlook rather than a deterministic price target.

### Key Functionalities
- **Live Data Ingestion:** Automated pipeline using `yfinance` API with multi-index handling.
- **Statistical Analysis:** Interactive return density plots overlaid with theoretical Gaussian curves to identify empirical fat-tails.
- **Risk Assessment:** Dynamic calculation of 95% Confidence Intervals and Value-at-Risk (VaR).
- **Macro Sensitivity:** Integrated drift adjustment parameters to simulate forward-looking economic scenarios.

## Development Iterations & Debugging

The project evolved through several technical challenges:

**Data Pipeline Robustness**
Initially, the app faced `KeyError` issues due to yfinance's multi-level column headers. The logic was refactored to flatten index structures, ensuring stable data flow for complex tickers like `VFV.TO`.

**Interactive Visualization**
Static Matplotlib plots were replaced with Plotly to enable precise data inspection. By configuring `spikemode` and `spikesnap`, the dashboard now allows for granular analysis of return densities at the 4th decimal place.

**Error Handling**
To handle API edge cases (e.g., weekends or invalid tickers), defensive programming was implemented to catch empty DataFrames and `IndexError` exceptions, replacing raw tracebacks with clean user notifications.

**Model Integration**
The standard GBM model was extended to include a 'Macro Bias' slider, bridging the gap between historical statistical drift and subjective macro-economic forecasting.

## Stack
- Python (NumPy, Pandas, SciPy)
- Plotly (Visualization)
- Streamlit (Deployment)

---
Developed by XXStvXX, *UTSC 28', 
Major in Statistics & Economics | Minor in English-Chinese Translation*
