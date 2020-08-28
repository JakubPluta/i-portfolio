import pandas as pd
import numpy as np


class WeightsOptimizer:
    
    """Class that takes as input tickers which are list or string, and weights.
    And it creates dictionary with tickers as key and weight as value
    If weights are not provided they are set to equal:
       * equal weight = 1 / divided by number of tickers 
    If weights are set it packs tickers and weights into dictionary. There are some validators that check if the 
    sum of weights is equal to 1, if no it's re-calculate weights with simple algorithm 
    """

    def __init__(self, tickers: (list, str), weights=None):
        self.__tickers = tickers
        self.__number_of_tickers = len(set(tickers))
        self.__weights = weights
        self.__ticker_weights_map = {}

        if not self.__weights and self.__tickers:
            self.__create_equal_weights()
            
        elif self.__weights and self.__tickers and len(self.__tickers) == len(self.__weights):
            self.__zip_portfolio()
            
        if sum(self.__weights) != 1:
            self.__repair_weights()
                 
    def get_weights(self):
        return self.__weights

    def get_portfolio(self):
        return self.__ticker_weights_map

    def create_portfolio(self, items: dict):
        if items:
            self.__ticker_weights_map = items

    def create_random_weights(self):
        weights = np.array(np.random.random(self.__number_of_tickers))
        self.__weights = weights/np.sum(weights)
        self.__zip_portfolio()
        
    def set_weights(self, stock: dict):
        for ticker, weight in stock.items():
            self.__ticker_weights_map[ticker] = weight
            
        self.__tickers, self.__weights = zip(*self.__ticker_weights_map.items())
        
        if sum(self.__weights) != 1:
            self.__repair_weights()
    
    @staticmethod    
    def __validate_bounds(weights):
        if sum(weights) != 1 or sum(weights) != 0.9999999999999999:
            raise ValueError("Sum of weights need to be equal to 1")
          
    def __create_equal_weights(self):
        self.__weights = np.array([1/self.__number_of_tickers for n in enumerate(self.__tickers)])
        self.__ticker_weights_map = dict(zip(self.__tickers, self.__weights))
        
    def __zip_portfolio(self):
        self.__ticker_weights_map = dict(zip(self.__tickers, self.__weights))
   
    def __repair_weights(self):
        if sum(self.__weights) < 1: 
            eq_add = (1 - sum(self.__weights))/self.__number_of_tickers
            self.__weights = [weight + eq_add for weight in self.__weights]
        elif sum(self.__weights) > 1:
            eq_add = (sum(self.__weights)-1)/self.__number_of_tickers
            self.__weights = [weight - eq_add for weight in self.__weights]
        self.__zip_portfolio()
    
       
        


