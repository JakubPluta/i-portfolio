from stock import Stock
from weights_optimizer import WeightsOptimizer

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

        self.__tickers = []
        self.__amounts = []
        self.__weights = []
        self.__portfolio = {}
        self.__total_investment = None

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

    def calculate_cov(self):
        returns = {}

        for ticker in self.__tickers:
            returns[ticker] = Stock(ticker).log_daily_returns["Close"].to_list()

        returns_df = pd.DataFrame(returns)
        covariance = returns_df.cov()
        return covariance

    def calculate_std(self):
        pass

    def calculate_expected_returns(self):
        pass

