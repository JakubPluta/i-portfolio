from portfolio import Portfolio
from stock import Stock



def test_portfolio_should_be_created():
    # given
    tickers = ["AMZN", "AAPL", "FB"]
    amounts = [10000,50000,30000]

    # when
    portfolio = Portfolio()

    portfolio.create_portfolio(tickers, amounts)

    assert portfolio
    assert len(tickers) == portfolio.ASSETS == len(portfolio._Portfolio__tickers)
    assert sum(portfolio._Portfolio__weights) in [1, 0.9999999999, 1.0000000000000002]
