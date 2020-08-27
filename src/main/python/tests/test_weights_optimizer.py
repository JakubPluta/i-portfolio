from weights_optimizer import WeightsOptimizer



def test_weights_opt():
    # given tickers
    tickers = ["AMZN", "FB", "AAPL"]

    wopt = WeightsOptimizer(tickers=tickers)

    portfolio = wopt.get_portfolio()
    weights = wopt.get_weights()

    assert wopt
    assert sum(portfolio.values()) == 1
    assert sum(weights) == 1


def test_weights_opt2():
    # given tickers

    weights = [0.1, 0.2, 0.11, 0.3, 0.09]
    tickers = ["AMZN", "FB", "GOOG", "SGP", "GM"]

    wopt = WeightsOptimizer(tickers,weights)

    wopt.set_weights({
        "AMZN": 0.4, "FB" : 0.22
    })

    portfolio = wopt.get_portfolio()
    weights = wopt.get_weights()

    assert wopt
    assert sum(portfolio.values()) == 1 or sum(portfolio.values()) == 0.9999999999999999
    assert sum(weights) in  [1, 0.9999999999999999 ]
