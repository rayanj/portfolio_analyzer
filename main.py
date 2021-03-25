#import position_manager as pm
import portfolio_analytics as pa
import matplotlib.pyplot as plt


#manager = pm.PortfolioManager()
#symbols = manager.get_expanded_symbols()
#print(symbols)
analytics = pa.PortfolioAnalytics()

tickers = analytics.get_ticker_from_portfolio()
print(tickers)

data = analytics.download_data(tickers)

norm = analytics.get_normalized_data(data)
print(norm)
norm.plot()
plt.show()
print(norm)


