from returns import *
from stock import Stock

def test_calculate_daily_returns():
    # given

    stock = Stock("AMZN")
    quotes = stock.get_quotes()

    daily_returns = calculate_daily_returns(quotes)
    daily_log_returns = calculate_daily_logarithmic_returns(quotes)
    assert not daily_returns.empty
    assert not daily_log_returns.empty
