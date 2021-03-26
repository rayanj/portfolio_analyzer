import portfolio_analytics as pa
import position_manager as pm
import yfinance as yf
import pandas as pd

analytics = pa.PortfolioAnalytics()
print('Getting top holdings...')
manager = pm.PortfolioManager()
portfolio = manager.get_sorted_portfolio()

holdings = analytics.get_Top_holdings_from_portfolio()
holdings.to_csv('portfolio_top_holdings.csv')

print('Extracting tickers from holdings...')
tickers = analytics.extract_tickers_from_holdings(holdings)
tickers = str(tickers).strip()
stocks = yf.Tickers(tickers).tickers
print(stocks)
sectors = []
for ticker in stocks:
    try:
        print(ticker)
        info = ticker.info
        sectors.append({
            'symbol': info['symbol'],
            'sector': info['sector']}
        )
    except:
        print('bad symbol:')
        continue



sectors = pd.DataFrame(sectors, columns=['symbol', 'sector'])
print(sectors)
portfolio.set_index('symbol')
sectors.set_index('symbol')

portfolio = portfolio.merge(sectors, on='symbol', how='inner')
print(portfolio)
grouped_portfolio = analytics.get_aggregated_portfolio(portfolio, ['sector','symbol'])
aggregated_portfolio = grouped_portfolio.sum()
manager.export_portfolio(portfolio, 'portfolio.csv')
manager.export_portfolio(aggregated_portfolio, 'aggregated_portfolio.csv')
print('Generating Daily Returns...')
data = analytics.download_data(tickers)
returns = analytics.get_daily_returns(data)
print(returns)
print('Generating Daily Risk...')
risk = analytics.get_anualized_risk(returns)
risk.to_csv('portfolio_risk.csv')
print(risk)
