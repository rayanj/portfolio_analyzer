import position_manager as pm
import pandas as pd
import yfinance as yf
import requests as re
import matplotlib.pyplot as plt
import numpy as np

class PortfolioAnalytics:
    def get_ticker_from_portfolio(self):
        manager = pm.PortfolioManager()
        tickers = manager.get_expanded_symbols().drop(index=[28, 29])
        tickers = pd.DataFrame(tickers, columns=['symbol'], )
        # tickers.reset_index(level=0, inplace=True)
        return tickers.to_csv(sep=',', index=False, header=False)


    def download_data(self, tickers):
        stocks = yf.download(tickers, period="1y").Close
        return stocks.head()

    def get_normalized_data(self, data):
        return data.div(data.iloc[0]).mul(100)