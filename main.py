import portfolio_analytics as pa

analytics = pa.PortfolioAnalytics()
print('Getting top holdings...')
holdings = analytics.get_Top_holdings_from_portfolio()
holdings.to_csv('portfolio_top_holdings.csv')

print('Extracting tickers from holdings...')
tickers = analytics.extract_tickers_from_holdings(holdings)
print('Generating Daily Returns...')
data = analytics.download_data(tickers)
returns = analytics.get_daily_returns(data)
print(returns)
print('Generating Daily Risk...')
risk = analytics.get_anualized_risk(returns)
risk.to_csv('portfolio_risk.csv')
print(risk)


