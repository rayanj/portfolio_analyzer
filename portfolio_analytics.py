import pandas as pd
import yfinance as yf
import numpy as np
import position_manager as pm


class PortfolioAnalytics:
    def get_Top_holdings_from_portfolio(self):
        manager = pm.PortfolioManager()
        return manager.get_expanded_symbols()

    def extract_tickers_from_holdings(self, holdings):
        tickers = pd.DataFrame(holdings, columns=['symbol'])[:50]
        return tickers.to_csv(sep=',', index=False, header=False)

    def download_data(self, tickers):
        stocks = yf.download(tickers, start='2020-3-25')
        print(stocks['Adj Close'])
        return stocks['Adj Close']  # .tail(20)

    def get_normalized_data(self, data):
        return data.div(data.iloc[0]).mul(100)

    def get_daily_returns(self, data):
        return np.log(data / data.shift(1))

    def get_anualized_risk(self, returns):
        risk = pd.DataFrame(columns=['mean', 'std', 'correlation', 'covariance'])
        risk['mean'] = returns.mean() * 250 * 100
        risk['std'] = returns.std() * 250 ** 0.5 * 100
        risk['correlation'] = returns.corr() * 250 ** 0.5
        risk['covariance'] = returns.cov() * 250 ** 0.5
        risk.index.name = 'symbol'
        risk.reset_index(level=0, inplace=True)
        return pd.DataFrame(risk.sort_values(by=['std'], ignore_index=False, ascending=False),
                            columns=['symbol', 'mean', 'std', 'correlation', 'covariance'])

    def get_aggregated_portfolio(self, portfolio, columns):
        return portfolio.groupby(columns, as_index=False)
