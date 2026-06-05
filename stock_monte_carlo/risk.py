from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class RiskReport:
    current_price: float
    expected_terminal_price: float
    expected_return: float
    median_terminal_price: float
    value_at_risk_95: float
    conditional_value_at_risk_95: float
    probability_of_loss: float
    probability_target_hit: float | None
    downside_price_5: float
    upside_price_95: float


def summarize_risk(
    current_price: float,
    terminal_prices: pd.Series,
    target_price: float | None = None,
) -> RiskReport:
    """Summarize terminal-path risk from a Monte Carlo simulation."""

    if current_price <= 0:
        raise ValueError("current_price must be positive.")
    if terminal_prices.empty:
        raise ValueError("terminal_prices cannot be empty.")

    terminal = pd.to_numeric(terminal_prices, errors="coerce").dropna()
    terminal_returns = terminal / current_price - 1
    p05 = float(terminal.quantile(0.05))
    p95 = float(terminal.quantile(0.95))
    var_return = float(terminal_returns.quantile(0.05))
    tail_returns = terminal_returns[terminal_returns <= var_return]
    cvar = float(tail_returns.mean()) if not tail_returns.empty else var_return

    probability_target_hit = None
    if target_price is not None:
        probability_target_hit = float((terminal >= target_price).mean())

    expected_terminal_price = float(terminal.mean())
    return RiskReport(
        current_price=float(current_price),
        expected_terminal_price=expected_terminal_price,
        expected_return=float(expected_terminal_price / current_price - 1),
        median_terminal_price=float(terminal.median()),
        value_at_risk_95=var_return,
        conditional_value_at_risk_95=cvar,
        probability_of_loss=float((terminal < current_price).mean()),
        probability_target_hit=probability_target_hit,
        downside_price_5=p05,
        upside_price_95=p95,
    )
