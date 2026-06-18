# Stock Monte Carlo Forecaster

A quantitative finance project for simulating stock price paths, studying downside risk, and building scenario-based forecasts with Geometric Brownian Motion (GBM). The default example is `VFV.TO`, but the app works with any ticker supported by Yahoo Finance.

This project started as an interactive Streamlit experiment and has been expanded into a small Python package with reusable modules, a CLI, tests, model notes, GitHub Actions CI, and a GitHub Pages project site.

## Live Links

- Live Streamlit app: https://stockmontecarloforecaster-xxstvxx.streamlit.app/
- Project site: https://xxstvxx.github.io/Stock_Monte_Carlo_Forecaster/
- Repository: https://github.com/XXStvXX/Stock_Monte_Carlo_Forecaster

## What It Does

- Downloads historical close prices with `yfinance`.
- Estimates daily drift and volatility from historical returns.
- Runs thousands of GBM Monte Carlo paths with a reproducible random seed.
- Lets the user apply an annualized macro bias for stress testing.
- Reports expected return, median outcome, 5th/95th percentile prices, VaR, CVaR, probability of loss, and target-hit probability.
- Visualizes both historical return distributions and future simulated price paths.

## AI-Assisted Workflow

This project uses AI-assisted prototyping and documentation as part of a human-in-the-loop workflow. AI helped speed up iteration around package structure, documentation, test planning, and UI explanation, while model assumptions, risk interpretation, and final technical claims remain manually reviewed.

See [`docs/AI_ASSISTED_WORKFLOW.md`](docs/AI_ASSISTED_WORKFLOW.md) for the workflow note.

## App Preview

Run the dashboard locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Or install the package in editable mode:

```bash
pip install -e ".[dev]"
streamlit run app.py
```

## Command Line Usage

```bash
stock-forecast VFV.TO --lookback-days 1095 --horizon-days 252 --paths 2000 --annual-macro-bias 0.02 --target-price 180
```

Example JSON scenario settings are available in [`examples/scenario_config.json`](examples/scenario_config.json).

## Project Structure

```text
.
├── app.py                         # Streamlit dashboard
├── site/index.html                # GitHub Pages project site
├── stock_monte_carlo/
│   ├── data.py                    # Yahoo Finance data loading and cleaning
│   ├── simulation.py              # GBM Monte Carlo engine
│   ├── risk.py                    # VaR, CVaR, probability metrics
│   ├── plotting.py                # Plotly chart builders
│   └── cli.py                     # Command line interface
├── tests/                         # Unit tests for simulation and risk logic
├── docs/MODEL_NOTES.md            # Model assumptions and limitations
├── pyproject.toml                 # Package metadata and tool config
└── .github/workflows/             # CI and Pages deployment workflows
```

## Methodology

The model uses GBM log-return dynamics:

```text
S_t = S_0 * exp(cumsum((mu - 0.5 * sigma^2) + sigma * Z_t))
```

The goal is not to predict one exact future price. The goal is to estimate a distribution of possible future prices and make uncertainty visible through quantiles, tail-risk metrics, and scenario controls.

## Tests

```bash
pytest -q
ruff check .
```

The CI workflow runs tests on Python 3.10, 3.11, and 3.12.

## Disclaimer

This project is for education and research. It is not financial advice. GBM assumes stable volatility and normally distributed log returns, while real markets include regime changes, jumps, liquidity constraints, and macro shocks.

## Author

XXStvXX (UTSC 2028)  
Major in Statistics & Economics | Minor in English-Chinese Translation
