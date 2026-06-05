import pandas as pd

from stock_monte_carlo import summarize_risk


def test_risk_report_computes_probabilities():
    terminal = pd.Series([80, 90, 100, 110, 120])
    report = summarize_risk(100, terminal, target_price=110)

    assert report.expected_terminal_price == 100
    assert report.expected_return == 0
    assert report.probability_of_loss == 0.4
    assert report.probability_target_hit == 0.4
    assert report.downside_price_5 < report.median_terminal_price
    assert report.upside_price_95 > report.median_terminal_price


def test_risk_report_handles_no_target():
    report = summarize_risk(100, pd.Series([95, 100, 105]))

    assert report.probability_target_hit is None
