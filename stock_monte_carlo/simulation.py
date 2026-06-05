from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class SimulationConfig:
    """Parameters for a geometric Brownian motion simulation."""

    horizon_days: int = 252
    paths: int = 1000
    annual_macro_bias: float = 0.0
    seed: int | None = 42

    def validate(self) -> None:
        if self.horizon_days < 1:
            raise ValueError("horizon_days must be positive.")
        if self.paths < 10:
            raise ValueError("paths must be at least 10.")
        if not -1.0 <= self.annual_macro_bias <= 1.0:
            raise ValueError("annual_macro_bias must be between -1.0 and 1.0.")


@dataclass(frozen=True)
class SimulationResult:
    """Matrix of simulated prices plus summary paths."""

    prices: pd.DataFrame
    mean_path: pd.Series
    lower_path: pd.Series
    upper_path: pd.Series
    terminal_prices: pd.Series

    @property
    def horizon_days(self) -> int:
        return len(self.prices)

    @property
    def paths(self) -> int:
        return self.prices.shape[1]


def run_gbm_simulation(
    last_price: float,
    daily_drift: float,
    daily_volatility: float,
    config: SimulationConfig | None = None,
) -> SimulationResult:
    """Generate future price paths using geometric Brownian motion.

    The model uses log-return dynamics so simulated prices remain positive.
    The macro bias is an annualized drift adjustment distributed across 252
    trading days.
    """

    cfg = config or SimulationConfig()
    cfg.validate()

    if last_price <= 0:
        raise ValueError("last_price must be positive.")
    if daily_volatility < 0:
        raise ValueError("daily_volatility cannot be negative.")

    rng = np.random.default_rng(cfg.seed)
    adjusted_daily_drift = daily_drift + cfg.annual_macro_bias / 252
    shocks = rng.normal(0.0, 1.0, size=(cfg.horizon_days, cfg.paths))
    log_returns = (adjusted_daily_drift - 0.5 * daily_volatility**2) + daily_volatility * shocks
    price_paths = last_price * np.exp(np.cumsum(log_returns, axis=0))

    index = pd.RangeIndex(1, cfg.horizon_days + 1, name="trading_day")
    columns = [f"path_{i + 1}" for i in range(cfg.paths)]
    prices = pd.DataFrame(price_paths, index=index, columns=columns)

    mean_path = prices.mean(axis=1).rename("mean")
    lower_path = prices.quantile(0.05, axis=1).rename("p05")
    upper_path = prices.quantile(0.95, axis=1).rename("p95")
    terminal_prices = prices.iloc[-1].rename("terminal_price")

    return SimulationResult(
        prices=prices,
        mean_path=mean_path,
        lower_path=lower_path,
        upper_path=upper_path,
        terminal_prices=terminal_prices,
    )
