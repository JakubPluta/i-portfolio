from cvxpy import *


class MarkowitzPortfolio():

    def __init__(self, mean_returns, covariance_matrix, trading_days=252):
        self.__risk_free = 0.003
        self.__mean_returns = mean_returns
        self.__covariance_matrix = covariance_matrix
        self.__trading_days = trading_days
