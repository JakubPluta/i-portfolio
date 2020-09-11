from cvxpy import *
import numpy as np
import pandas as pd


class MarkowitzPortfolio():

    def __init__(self, num_assets, mean_returns, covariance_matrix, trading_days=252, n_simulations=1000):
        self.__risk_free = 0.003
        self.__mean_returns = mean_returns
        self.__covariance_matrix = covariance_matrix
        self.__trading_days = trading_days
        self.__n_simulations = n_simulations
        self.__num_assets = num_assets

    def weights(self):
        return np.random.dirichlet(np.ones(self.__num_assets), size=1)[0]

    def optimize(self):
        port_returns = []
        port_vols = []
        sharpes = []
        port_weights = []

        for _ in range(self.__n_simulations):
            weights = self.weights()
            portfolio_return = np.sum(self.__mean_returns * weights) * 252
            portfolio_std = np.sqrt(np.dot(weights, np.dot(self.__covariance_matrix, weights))) * np.sqrt(252)
            port_returns.append(port_returns)
            port_vols.append(portfolio_std)
            sharpes.append(portfolio_return/portfolio_std)
            port_weights.append(weights)

        return pd.DataFrame(
            {
                "Weights" : port_weights,
                "Returns" : port_returns,
                "STD" : port_vols,
                "Sharpes" : sharpes,


            }
        )