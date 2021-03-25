import position_manager as pm
import pandas as pd
import yfinance as yf
import requests as re
import matplotlib.pyplot as plt
import numpy as np

manager = pm.PortfolioManager()
tickers = manager.get_expanded_symbols().drop(index=[28,29])
tickers = pd.DataFrame(tickers, columns=['symbol'],)
#tickers.reset_index(level=0, inplace=True)
tickers = tickers.to_csv(sep=',', index=False, header=False)
print(tickers)
stocks = yf.download(tickers, period="1y").Close
hed=stocks.head()

norm=hed.div(hed.iloc[0]).mul(100)
print(norm)
norm.plot()
plt.show()


