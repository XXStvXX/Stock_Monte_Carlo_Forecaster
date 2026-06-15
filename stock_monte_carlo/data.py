from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import yfinance as yf


@dataclass(frozen=True)
class MarketData:
    """Clean market series used by the forecasting model."""

    ticker: str
    prices: pd.Series
    returns: pd.Series
    start_date: str
    end_date: str

    @property
    def last_price(self) -> float:
        return float(self.prices.iloc[-1])

    @property
    def daily_drift(self) -> float:
        return float(self.returns.mean())

    @property
    def daily_volatility(self) -> float:
        return float(self.returns.std(ddof=1))

    @property
    def annualized_drift(self) -> float:
        return float(self.daily_drift * 252)

    @property
    def annualized_volatility(self) -> float:
        return float(self.daily_volatility * np.sqrt(252))


def _close_column(data: pd.DataFrame, ticker: str) -> pd.Series:
    if data.empty:
        raise ValueError(f"No price data returned for {ticker}.")

    if isinstance(data.columns, pd.MultiIndex):
        if ("Close", ticker) in data.columns:
            prices = data[("Close", ticker)]
        else:
            prices = data["Close"].iloc[:, 0]
    else:
        prices = data["Close"]

    prices = pd.to_numeric(prices, errors="coerce").dropna()
    if prices.empty:
        raise ValueError(f"No usable closing prices returned for {ticker}.")
    return prices


def load_market_data(
    ticker: str, lookback_days: int = 365, end: datetime | None = None
) -> MarketData:
    """Download historical prices and compute daily simple returns."""

    clean_ticker = ticker.strip().upper()
    if not clean_ticker:
        raise ValueError("Ticker cannot be empty.")
    if lookback_days < 30:
        raise ValueError("lookback_days must be at least 30.")

    end_dt = end or datetime.now()
    start_dt = end_dt - timedelta(days=lookback_days)
    start_date = start_dt.strftime("%Y-%m-%d")
    end_date = end_dt.strftime("%Y-%m-%d")

    raw = yf.download(
        clean_ticker, start=start_date, end=end_date, auto_adjust=False, progress=False
    )
    prices = _close_column(raw, clean_ticker)
    returns = prices.pct_change().replace([np.inf, -np.inf], np.nan).dropna()

    if len(returns) < 20:
        raise ValueError("Not enough return observations to estimate drift and volatility.")

    return MarketData(
        ticker=clean_ticker,
        prices=prices,
        returns=returns,
        start_date=start_date,
        end_date=end_date,
    )
