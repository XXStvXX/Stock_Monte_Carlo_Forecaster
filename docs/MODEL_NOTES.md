# Model Notes

This project uses geometric Brownian motion (GBM) as a transparent baseline for probabilistic forecasting. It is not designed to predict an exact stock price. It estimates a distribution of possible outcomes based on historical drift, historical volatility, and an optional forward-looking macro drift adjustment.

## Core Equation

The simulation uses log-return dynamics:

```text
S_t = S_0 * exp(cumsum((mu - 0.5 * sigma^2) + sigma * Z_t))
```

Where:

- `S_0` is the latest observed close.
- `mu` is the estimated daily drift plus any daily macro adjustment.
- `sigma` is the estimated daily volatility.
- `Z_t` is a random draw from the standard normal distribution.

## Reported Metrics

- Expected terminal price: mean simulated price at the forecast horizon.
- Median terminal price: midpoint of the simulated terminal distribution.
- 5th and 95th percentile prices: a 90% simulation interval.
- VaR 95%: the 5th percentile terminal return.
- CVaR 95%: average return inside the worst 5% of terminal outcomes.
- Probability of loss: share of paths ending below the current price.
- Probability target hit: share of paths ending at or above a user-selected target price.

## Limitations

GBM assumes normally distributed log returns and constant volatility. Real markets show regime changes, volatility clustering, jumps, transaction costs, liquidity constraints, and macro shocks. For this reason, the app should be read as a risk exploration tool, not financial advice.

## Extension Ideas

- Add regime-switching volatility.
- Compare GBM against bootstrapped historical returns.
- Add portfolio-level covariance simulation.
- Add backtesting that compares forecast intervals against realized outcomes.
- Save scenario runs to CSV for reproducible reports.
