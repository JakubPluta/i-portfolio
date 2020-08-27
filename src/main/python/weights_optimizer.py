import pandas as pd
import numpy as np


class WeightsOptimizer:

    def __init__(self, tickers: (list, str), weights=None):
        self.__tickers = tickers
        self.__number_of_tickers = len(set(tickers))
        self.__weights = weights
        self.__ticker_weights_map = {}

        if not self.__weights and self.__tickers:
            self.__create_equal_weights()
            
        elif self.__weights and self.__tickers and len(self.__tickers) == len(self.__weights):
            self.__zip_portfolio()
                  
    def __create_equal_weights(self):
        self.__weights = np.array([1/self.__number_of_tickers for n in enumerate(self.__tickers)])
        self.__ticker_weights_map = dict(zip(self.__tickers, self.__weights))
        
    def __zip_portfolio(self):
        self.__ticker_weights_map = dict(zip(self.__tickers, self.__weights))
        
    @staticmethod    
    def __validate_bounds(weights):
        if sum(weights) != 1:
            raise ValueError("Sum of weights need to be equal to 1")
    
    def show_weights(self):
        return self.__weights

    def show_portfolio(self):
        return self.__ticker_weights_map

    def set_weights(self, weights: dict):
        if weights:
            self.__validate_bounds(weights.values())
        self.__ticker_weights_map = weights
        
        
    
        
        


