from __future__ import annotations

import streamlit as st

from stock_monte_carlo import (
    SimulationConfig,
    load_market_data,
    run_gbm_simulation,
    summarize_risk,
)
from stock_monte_carlo.plotting import returns_distribution_chart, simulation_chart


LOOKBACK_OPTIONS = {
    "3 months": 90,
    "6 months": 180,
    "1 year": 365,
    "3 years": 365 * 3,
    "5 years": 365 * 5,
    "Max sample": 365 * 15,
}


st.set_page_config(page_title="Quant Research Lab", layout="wide")
st.title("Quant Research Lab")
st.caption(
    "Monte Carlo forecasting, downside risk, and scenario analysis for liquid equity tickers."
)

with st.sidebar:
    st.header("Market")
    ticker = st.text_input("Ticker", "VFV.TO")
    lookback_label = st.selectbox("Historical sample", list(LOOKBACK_OPTIONS), index=2)

    st.header("Simulation")
    horizon_days = st.slider("Forecast horizon", 20, 504, 252, help="Trading days into the future.")
    paths = st.slider("Simulation paths", 100, 5000, 1000, step=100)
    annual_macro_bias = st.slider(
        "Annual macro bias",
        -0.30,
        0.30,
        0.0,
        step=0.01,
        format="%.2f",
        help="Annualized drift adjustment used for stress testing.",
    )
    seed = st.number_input("Random seed", min_value=0, max_value=999999, value=42, step=1)
    target_price = st.number_input("Optional target price", min_value=0.0, value=0.0, step=1.0)

if ticker:
    try:
        with st.spinner(f"Downloading and modelling {ticker.upper()}..."):
            market = load_market_data(ticker, LOOKBACK_OPTIONS[lookback_label])
            config = SimulationConfig(
                horizon_days=horizon_days,
                paths=paths,
                annual_macro_bias=annual_macro_bias,
                seed=int(seed),
            )
            result = run_gbm_simulation(
                last_price=market.last_price,
                daily_drift=market.daily_drift,
                daily_volatility=market.daily_volatility,
                config=config,
            )
            risk = summarize_risk(
                market.last_price,
                result.terminal_prices,
                target_price=target_price if target_price > 0 else None,
            )
    except Exception as exc:  # Streamlit should surface data/provider issues clearly.
        st.error(str(exc))
        st.stop()

    kpi_cols = st.columns(5)
    kpi_cols[0].metric("Current", f"${risk.current_price:,.2f}")
    kpi_cols[1].metric(
        "Expected", f"${risk.expected_terminal_price:,.2f}", f"{risk.expected_return:.2%}"
    )
    kpi_cols[2].metric("Median", f"${risk.median_terminal_price:,.2f}")
    kpi_cols[3].metric("VaR 95%", f"{risk.value_at_risk_95:.2%}", delta_color="inverse")
    kpi_cols[4].metric("Prob. loss", f"{risk.probability_of_loss:.1%}", delta_color="inverse")

    tab_forecast, tab_distribution, tab_risk, tab_data = st.tabs(
        ["Forecast", "Return distribution", "Risk report", "Data"]
    )

    with tab_forecast:
        st.plotly_chart(simulation_chart(result), use_container_width=True)

    with tab_distribution:
        st.plotly_chart(returns_distribution_chart(market.returns), use_container_width=True)

    with tab_risk:
        left, right = st.columns(2)
        with left:
            st.subheader("Downside")
            st.metric("5th percentile terminal price", f"${risk.downside_price_5:,.2f}")
            st.metric(
                "Conditional VaR 95%",
                f"{risk.conditional_value_at_risk_95:.2%}",
                delta_color="inverse",
            )
        with right:
            st.subheader("Upside")
            st.metric("95th percentile terminal price", f"${risk.upside_price_95:,.2f}")
            if risk.probability_target_hit is not None:
                st.metric("Probability target is hit", f"{risk.probability_target_hit:.1%}")
            else:
                st.info("Enter a target price in the sidebar to estimate hit probability.")

    with tab_data:
        st.write(
            {
                "ticker": market.ticker,
                "sample_start": market.start_date,
                "sample_end": market.end_date,
                "observations": int(len(market.returns)),
                "annualized_drift": f"{market.annualized_drift:.2%}",
                "annualized_volatility": f"{market.annualized_volatility:.2%}",
            }
        )
        st.dataframe(market.prices.rename("close").tail(30), use_container_width=True)
