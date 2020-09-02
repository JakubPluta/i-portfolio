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

    def create_portfolio(self, tickers: list, amounts: list):
        if len(tickers) == len(amounts):
            [self.__tickers.append(ticker) for ticker in tickers]
            self.__amounts = amounts
            self._update_portfolio()
            self.ASSETS = len(tickers)

    def get_portfolio_items(self):
        return self.__portfolio

    def get_weights(self):
        return self.__weights

    def get_tickers(self):
        return self.__tickers

    def get_total_amount_invested(self):
        return self.__total_investment

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
                             "All of weights was set-up into equal.\n"
                             "If you want to change weights use set_weights() method")



#TODO add New Class that creates Portfolio that Contains Stock objects, and weights
class InvPortfolio(Portfolio):
    pass