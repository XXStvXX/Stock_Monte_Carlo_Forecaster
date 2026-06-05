from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from scipy.stats import norm

from .simulation import SimulationResult


def returns_distribution_chart(returns: pd.Series) -> go.Figure:
    clean_returns = pd.to_numeric(returns, errors="coerce").dropna()
    mu = float(clean_returns.mean())
    sigma = float(clean_returns.std(ddof=1))
    x_range = np.linspace(float(clean_returns.min()), float(clean_returns.max()), 200)
    y_norm = norm.pdf(x_range, mu, sigma)

    fig = go.Figure()
    fig.add_trace(
        go.Histogram(
            x=clean_returns,
            nbinsx=90,
            name="Actual returns",
            marker_color="#2f6f73",
            opacity=0.72,
            histnorm="probability density",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_range,
            y=y_norm,
            mode="lines",
            name="Normal fit",
            line=dict(color="#b23a48", width=2.5),
        )
    )
    fig.update_layout(
        template="simple_white",
        hovermode="x unified",
        height=420,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(title="Daily return", tickformat=".2%", showspikes=True, spikedash="dash"),
        yaxis=dict(title="Density", gridcolor="rgba(180,180,180,0.25)"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig


def simulation_chart(result: SimulationResult, max_paths: int = 120) -> go.Figure:
    fig = go.Figure()
    sample = result.prices.iloc[:, : min(max_paths, result.paths)]

    for column in sample.columns:
        fig.add_trace(
            go.Scatter(
                x=sample.index,
                y=sample[column],
                mode="lines",
                line=dict(color="rgba(47,111,115,0.08)", width=1),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    fig.add_trace(
        go.Scatter(
            x=result.mean_path.index,
            y=result.mean_path,
            mode="lines",
            name="Expected mean",
            line=dict(color="#b23a48", width=3),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=result.upper_path.index,
            y=result.upper_path,
            mode="lines",
            name="95th percentile",
            line=dict(color="#263238", width=1.5, dash="dash"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=result.lower_path.index,
            y=result.lower_path,
            mode="lines",
            name="5th percentile",
            line=dict(color="#263238", width=1.5, dash="dash"),
            fill="tonexty",
            fillcolor="rgba(143, 122, 87, 0.18)",
        )
    )

    fig.update_layout(
        template="simple_white",
        height=520,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Trading days into future",
        yaxis_title="Simulated price",
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )
    return fig
