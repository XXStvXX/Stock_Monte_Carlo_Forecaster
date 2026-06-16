# Interview Notes: Stock Monte Carlo Forecaster

## 60-Second Explanation

I built the Stock Monte Carlo Forecaster to make uncertainty and downside risk more visible than a single price prediction.

The application downloads historical market data, estimates return and volatility assumptions, and simulates thousands of possible future price paths with a Geometric Brownian Motion model. It reports metrics such as Value at Risk, Conditional Value at Risk, probability of loss, target-hit probability, and percentile outcomes.

The goal is not to predict one exact future price. The goal is to show a distribution of possible outcomes, make downside scenarios easier to discuss, and document the limitations of the assumptions.

## Problem

A single expected return or target price can hide uncertainty. For early-stage investment or risk analysis, it is useful to ask:

- What range of outcomes is plausible under the model assumptions?
- How severe could the downside be in the simulated tail?
- How sensitive are outcomes to horizon, volatility, and scenario assumptions?

## Approach

1. Download historical close prices using `yfinance`.
2. Calculate historical returns.
3. Estimate drift and volatility from the return series.
4. Simulate future price paths using GBM dynamics.
5. Summarize the terminal price distribution and downside risk metrics.
6. Visualize historical returns, simulated paths, and scenario outcomes in Streamlit and Plotly.

## Key Metrics

- Expected return
- Median terminal price
- 5th and 95th percentile outcomes
- Value at Risk
- Conditional Value at Risk
- Probability of loss
- Target-hit probability

## Design Decisions

- I separated simulation, risk metrics, plotting, data loading, and CLI logic into reusable modules instead of keeping everything in one Streamlit file.
- I added tests for the simulation and risk logic so the project is easier to maintain.
- I added a command-line interface so the model can be run outside the dashboard.
- I documented limitations because the model should not be presented as financial advice.

## Limitations

- GBM assumes normally distributed log returns and stable volatility.
- Real markets can include jumps, regime changes, liquidity constraints, and macro shocks.
- Historical drift and volatility may not represent future conditions.
- Results should be interpreted as scenario analysis, not as a forecast guarantee.

## What I Would Improve Next

- Add a clearer example-results section to the README.
- Add screenshots or a short demo GIF.
- Compare GBM output with a historical bootstrap approach.
- Add sensitivity analysis for volatility and macro-bias assumptions.
- Add a small explanation panel for nontechnical users.

## Interview Questions To Prepare

### Why Monte Carlo?

Monte Carlo simulation is useful when the outcome is uncertain and we care about a distribution rather than one point estimate. It helps communicate downside risk, range of outcomes, and probability-based scenarios.

### What does VaR mean here?

Value at Risk estimates a loss threshold at a chosen confidence level under the simulated distribution. It is not a maximum possible loss; it is a model-based tail-risk summary.

### What is CVaR?

Conditional Value at Risk summarizes the average outcome in the tail beyond the VaR threshold. It gives more information about severity when losses are already in the tail.

### What did you personally build?

I built the Streamlit app, the simulation and risk modules, the command-line interface, the tests, the documentation, and the GitHub Actions workflow.
