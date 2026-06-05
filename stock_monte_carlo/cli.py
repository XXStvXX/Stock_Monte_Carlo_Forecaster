from __future__ import annotations

import argparse
import json

from .data import load_market_data
from .risk import summarize_risk
from .simulation import SimulationConfig, run_gbm_simulation


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a Monte Carlo forecast for a stock ticker.")
    parser.add_argument("ticker", help="Ticker symbol accepted by Yahoo Finance, e.g. VFV.TO or SPY.")
    parser.add_argument("--lookback-days", type=int, default=365)
    parser.add_argument("--horizon-days", type=int, default=252)
    parser.add_argument("--paths", type=int, default=1000)
    parser.add_argument("--annual-macro-bias", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--target-price", type=float, default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    market = load_market_data(args.ticker, lookback_days=args.lookback_days)
    config = SimulationConfig(
        horizon_days=args.horizon_days,
        paths=args.paths,
        annual_macro_bias=args.annual_macro_bias,
        seed=args.seed,
    )
    result = run_gbm_simulation(
        market.last_price,
        market.daily_drift,
        market.daily_volatility,
        config,
    )
    report = summarize_risk(market.last_price, result.terminal_prices, args.target_price)

    payload = {
        "ticker": market.ticker,
        "sample_start": market.start_date,
        "sample_end": market.end_date,
        "current_price": report.current_price,
        "expected_terminal_price": report.expected_terminal_price,
        "expected_return": report.expected_return,
        "value_at_risk_95": report.value_at_risk_95,
        "conditional_value_at_risk_95": report.conditional_value_at_risk_95,
        "probability_of_loss": report.probability_of_loss,
        "probability_target_hit": report.probability_target_hit,
    }
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
