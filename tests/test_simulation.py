import numpy as np

from stock_monte_carlo import SimulationConfig, run_gbm_simulation


def test_simulation_shape_and_positive_prices():
    result = run_gbm_simulation(
        last_price=100.0,
        daily_drift=0.0003,
        daily_volatility=0.012,
        config=SimulationConfig(horizon_days=30, paths=200, seed=7),
    )

    assert result.prices.shape == (30, 200)
    assert result.terminal_prices.shape[0] == 200
    assert np.isfinite(result.prices.to_numpy()).all()
    assert (result.prices.to_numpy() > 0).all()


def test_simulation_seed_is_reproducible():
    config = SimulationConfig(horizon_days=10, paths=50, seed=123)
    first = run_gbm_simulation(50.0, 0.0001, 0.01, config)
    second = run_gbm_simulation(50.0, 0.0001, 0.01, config)

    assert first.prices.equals(second.prices)


def test_macro_bias_changes_terminal_expectation():
    pessimistic = run_gbm_simulation(
        100.0,
        0.0,
        0.01,
        SimulationConfig(horizon_days=252, paths=500, annual_macro_bias=-0.15, seed=42),
    )
    optimistic = run_gbm_simulation(
        100.0,
        0.0,
        0.01,
        SimulationConfig(horizon_days=252, paths=500, annual_macro_bias=0.15, seed=42),
    )

    assert optimistic.terminal_prices.mean() > pessimistic.terminal_prices.mean()
