from portfolio import Portfolio
from stock import Stock



def test_portfolio_should_be_created_from_list():
    # given
    tickers = ["AMZN", "AAPL", "FB"]

    # when
    portfolio = Portfolio()

    portfolio.create_portfolio(tickers)

    assert portfolio
    assert len(tickers) == portfolio.ASSETS == len(portfolio._Portfolio__tickers)
    assert sum(portfolio._Portfolio__weights) in [1, 0.9999999999, 1.0000000000000002]


def test_portfolio_should_be_created_from_dict():
    # given
    tickers = {"AMZN" : 0.55, "AAPL": 0.22, "FB" : 0.38}

    # when
    portfolio = Portfolio()

    portfolio.create_portfolio(tickers)

    assert portfolio
    assert len(tickers.values()) == portfolio.ASSETS == len(portfolio._Portfolio__tickers)
    assert sum(portfolio._Portfolio__weights) in [1, 0.9999999999, 1.0000000000000002]
