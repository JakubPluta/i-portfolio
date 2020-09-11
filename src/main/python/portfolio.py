from stock import Stock
import numpy as np
import functools as ft
from metrics import METRICS_DICT
from markovitz import MarkowitzPortfolio

# https://blog.quantinsti.com/calculating-covariance-matrix-portfolio-variance/

# Portfolio metrics

# Annualised Returns
# Annualised Volatility
# Sharpe Ratio
# Sortino Ratio
# Beta
# Treynor Ratio
# Information Ratio
# Skewness
# Kurtosis
# Maximum Drawdown
# Number of Trades
# Profit ratio
# Holding period

import pandas as pd



class Portfolio:

    ASSETS = 0
    TRADING_DAYS = 252

    def __init__(self):
        """Portfolio should have tickers, amounts of investment like:
            tickers = ["AMZN", "FB", "GOOG"]
            amounts = [10000, 300000, 150000]
        """

        #TODO think about storing portfolio as dicts with 3 attr
        """ 
                portfolio = {
                "FB" : {"Stock: Stock("FB"), "Weight" : 0.2, Amount: 20000} ,
                "FB" : {"Stock: Stock("FB"), "Weight" : 0.2, Amount: 20000} ,
                "FB" : {"Stock: Stock("FB"), "Weight" : 0.2, Amount: 20000} ,
                }
        """

        self.__tickers: list = []
        self.__amounts: list = []
        self.__weights: list = []
        self.__portfolio: dict = {}
        self.__total_investment = None
        self.__returns: pd.DataFrame = None

    def create_portfolio(self, tickers: list, amounts: list):
        if len(tickers) == len(amounts):
            self.__tickers = tickers
            self.__amounts = amounts
            self._update_portfolio()
            self.ASSETS = len(tickers)

    def add_stock_to_portfolio(self, ticker: str, amount: (int, float)):
        """
        :param ticker: str ticker of company e.g facebook = FB
        :param amount: int/float amount of invested money
        :return: self.__portfolio: {"FB" : 10000}
        """
        if ticker not in self.__tickers:
            self.__tickers.append(ticker)
            self.__amounts.append(amount)
            self.ASSETS += 1
            self._update_portfolio()

    def delete_stock_from_portfolio(self, ticker: str):
        try:
            del self.__portfolio[ticker]
            self.ASSETS -= 1
            self.__tickers, self.__amounts = zip(*self.__portfolio.items())
            self._update_portfolio()
        except KeyError:
            print("Ticker not found")

    @property
    def amounts(self):
        return self.__weights

    @amounts.setter
    def amounts(self, amounts: list):
        if len(amounts) == len(self.__tickers):
            self.__amounts = amounts
        else:
            raise ValueError(f"Number of amounts is not equal to number of tickers\n"
                             f"List of tickers: {self.__tickers}\n"
                             f"List of amounts: {amounts}")

    @property
    def tickers(self):
        return self.__tickers

    @tickers.setter
    def tickers(self, tickers: list):
        if len(tickers) == len(self.__amounts):
            self.__tickers = tickers
        else:
            self.__tickers = tickers
            print(f"Ticker's are set to {self.__tickers}\n"
                  f"Now you need to set amounts")

    @property
    def portfolio(self):
        return self.__portfolio

    @portfolio.setter
    def portfolio(self, portfolio: dict):
        if portfolio:
            self.__tickers, self.__amounts = zip(*portfolio.items())
            self._update_portfolio()
            self.ASSETS = len(portfolio.keys())

    @portfolio.deleter
    def portfolio(self):
        print("Deleting portfolio")
        del self.portfolio
        self._update_portfolio()
        self.ASSETS = 0

    @property
    def weights(self):
        return self.__weights

    @weights.setter
    def weights(self, weights):
        if len(weights) == len(self.__tickers):
            self.__weights = weights
        self.__amounts = self.__total_investment * [self.__weights]
        self._update_portfolio()
        self.ASSETS = len(self.__amounts)

    @property
    def total_amount_invested(self):
        return self.__total_investment

    @total_amount_invested.setter
    def total_amount_invested(self, total_amount_invested):
        self.__total_investment = total_amount_invested
        self.__amounts = total_amount_invested * [self.__weights]

    def _update_portfolio(self):
        self.__calculate_weights()
        self.__calculate_total_amount_invested()
        self.__zip_portfolio()
        self.__get_portfolio_returns()

    def __calculate_total_amount_invested(self):
        self.__total_investment = sum(self.__amounts)

    def __calculate_weights(self):
        # It needs to be always equal to 1
        self.__weights = [amount/sum(self.__amounts) for amount in self.__amounts]

    def __zip_portfolio(self):
        if (self.__weights and self.__tickers) and (len(self.__amounts) == len(self.__amounts)):
            self.__portfolio = dict(zip(self.__tickers, self.__amounts))

    def __validate_weights(self):
        if not sum(self.__weights) == 1:
            raise ValueError("Weights of all assets needs to be equal to 1\n"
                             "All of weights were set-up into equal.\n"
                             "If you want to change weights go with weights, or amounts property")

    def __random_weights_portfolio(self):
        weights = np.array(np.random.random(len(self.__tickers)))
        self.__weights = weights / np.sum(weights)
        self.__zip_portfolio()

    @ft.lru_cache()
    def __get_portfolio_returns(self):
        """Log returns of portfolio assets calculated using closing prices
        :return: DataFrame with portfolio assets log returns
        """
        returns = {}
        for ticker in self.__tickers:
            returns[ticker] = Stock(ticker).log_daily_returns["Close"].to_list()
        self.__returns = pd.DataFrame(returns)

    @ft.lru_cache()
    def __get_key_metrics(self):
        metrics = {}
        for ticker in self.__tickers:
            metrics[ticker] = Stock(ticker)._get_metrics()
        return pd.DataFrame(metrics)

    def calculate_portfolio_metrics(self):
        return (self.__get_key_metrics() * self.__weights).mean(axis=1).to_dict()

    def calculate_portfolio_cov(self):
        """Calculate portfolio covariance matrix
        :return: DataFrame with covariance of portfolio assets
        """
        return self.__returns.cov()

    def calculate_portfolio_variance(self):
        """Portfolio variance is a measurement of risk, of how the aggregate actual returns of a
        set of securities making up a portfolio fluctuate over time.
        This portfolio variance statistic is calculated using the standard deviations of each security
        in the portfolio as well as the correlations of each security pair in the portfolio."""
        cov_annualized = self.calculate_portfolio_cov() * self.TRADING_DAYS
        return np.dot(self.__weights, np.dot(cov_annualized, self.__weights))

    def calculate_portfolio_volatility(self):
        """The volatility of a portfolio of stocks is a measure of how wildly the total
        value of all the stocks in that portfolio appreciates or declines.
        :return: Annualized Portfolio Volatility (Portfolio Risk)
        """
        return np.sqrt(np.dot(self.__weights,
                              np.dot(self.calculate_portfolio_cov()*self.TRADING_DAYS, self.__weights)))

    def calculate_portfolio_expected_returns(self):
        """The expected return of a portfolio is calculated by multiplying the weight of each asset
        by its expected return and adding the values for each investment.
        We return here annualized expected returns. So we multiply our results by 252 (number of trading days in year)
        Also can be calculated with formula: round(np.sum(mean_daily_returns * weights) * 252,2)
        :return: Annualized portfolio expected return
        """
        return np.dot(self.__returns.mean(), self.__weights) * self.TRADING_DAYS

    def calculate_portfolio_sharpe_ratio(self):
        return self.calculate_portfolio_expected_returns()/self.calculate_portfolio_volatility()

    def show_portfolio_statistics(self):
        print()
        print("Portfolio contains:\n"
              f"Tickers: {', '.join(self.__tickers)}\n"
              f"Amounts: {', '.join(map(str, self.__amounts))}\n"
              f"Weights: {', '.join(map(str, self.__weights))}\n"
              f"Portfolio Expected Returns: {round(self.calculate_portfolio_expected_returns(),2)}\n"
              f"Portfolio Variance: {round(self.calculate_portfolio_variance(),2)}\n"
              f"Portfolio Volatility: {round(self.calculate_portfolio_volatility(),2)}\n"
              f"Portfolio Sharpe Ratio: {round(self.calculate_portfolio_sharpe_ratio(),2)}")
        for metric, value in self.calculate_portfolio_metrics().items():
              print(f"Portfolio Weighted Average {METRICS_DICT.get(metric)}: {round(value,2)}")

    def optimize_markovitz_portfolio(self):
        mean_returns, cov, assets = self.__returns.mean(), self.calculate_portfolio_cov(), len(self.__tickers)
        return MarkowitzPortfolio(assets, cov, assets).optimize()

