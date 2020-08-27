from weights_optimizer import WeightsOptimizer



def test_weights_opt():
    # given tickers
    tickers = ["AMZN", "FB", "AAPL"]

    wopt = WeightsOptimizer(tickers=tickers)

    portfolio = wopt.show_portfolio()
    weights = wopt.show_weights()

    assert wopt
    assert sum(portfolio.values()) == 1
    assert sum(weights) == 1
