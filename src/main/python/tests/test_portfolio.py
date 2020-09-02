from portfolio import Portfolio
from stock import Stock
import pandas as pd


def test_portfolio_should_be_created():
    # given
    tickers = ["AMZN", "AAPL", "FB"]
    amounts = [10000,50000,30000]

    # when
    portfolio = Portfolio()

    portfolio.create_portfolio(tickers, amounts)

    assert portfolio
    assert len(tickers) == portfolio.ASSETS == len(portfolio._Portfolio__tickers)
    assert round(sum(portfolio._Portfolio__weights)) == 1


def test_stock_should_be_added():
    # given
    tickers = ["AMZN", "AAPL", "FB"]
    amounts = [10000,50000,30000]
    portfolio = Portfolio()
    portfolio.create_portfolio(tickers, amounts)

    portfolio.add_stock_to_portfolio(ticker="GOOG", amount=25000)

    assert portfolio.get_total_amount_invested() == 115000
    assert portfolio.ASSETS == 4
    assert round(sum(portfolio._Portfolio__weights)) == 1

def test_stock_should_be_deleted():
    # given
    tickers = ["AMZN", "AAPL", "FB"]
    amounts = [10000,50000,30000]
    portfolio = Portfolio()
    portfolio.create_portfolio(tickers, amounts)

    portfolio.delete_stock_from_portfolio(ticker="FB")
    cov = portfolio.calculate_cov()
    assert portfolio.get_total_amount_invested() == 60000
    assert portfolio.ASSETS == 2
    assert round(sum(portfolio._Portfolio__weights)) == 1
    assert isinstance(cov,pd.DataFrame)
