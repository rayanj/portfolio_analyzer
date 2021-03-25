import os
import pandas as pd
from yahooquery import Ticker


def sort_prices(holdings):
    return pd.DataFrame(holdings.sort_values(by=['market_value'], ignore_index=False, ascending=False),
                        columns=['quantity', 'regularMarketPrice', 'market_value'])


def read_positions():
    os.chdir(r"D:\DJDocs\Code\portfolios_analyzer\Data")
    print("Directory changed")
    path = "Portfolio_Position_Mar-16-2021.csv"
    return pd.read_csv(path)


def extract_stock_value(local_tickers, ticker):
    index = local_tickers.index[local_tickers['Symbol'] == ticker].tolist()[0]
    val = local_tickers.iloc[index]
    etf_holdings = pd.DataFrame(val.loc['Value'], columns=['symbol', 'holdingPercent'])
    etf_holdings['holdingPercent'] = etf_holdings['holdingPercent'].mul(val['Quantity'])
    etf_holdings.columns = ['symbol', 'quantity']
    return etf_holdings


class PositionAnalyzer:

    def __init__(self):
        self.portfolio = read_positions()
        self.tickers = self.portfolio[['Symbol', 'Quantity']][5:22]
        self.holdings = self.get_holdings()
        self.stocks = []
        self.etfs = pd.DataFrame(columns=['Symbol', 'Quantity', 'Value'])
        self.separate_stocks_and_etfs()

    def get_holdings(self):
        symbols = self.tickers['Symbol'][5:20]
        symbols = symbols.dropna().drop_duplicates()
        t = Ticker(symbols)
        return t.fund_top_holdings

    def separate_stocks_and_etfs(self):
        for holding in self.holdings:
            index = self.tickers.index[self.tickers['Symbol'] == holding].tolist()[0]
            quantity = self.tickers.loc[index, 'Quantity']
            if "No fundamentals data found for any of the summaryTypes=topHoldings" in self.holdings[holding]:
                self.stocks.append([holding, quantity])
            elif "holdings" in self.holdings[holding]:
                self.etfs.loc[len(self.etfs)] = [holding, quantity, self.holdings[holding]['holdings']]
            else:
                continue

    def get_aggregated_holdings(self, etfs, stocks):
        holdings = pd.DataFrame(columns=['symbol', 'quantity'])
        for etf in etfs['Symbol']:
            val = extract_stock_value(etfs, etf)
            holdings = pd.concat([holdings, val], ignore_index=True, sort=False)

        stks = pd.DataFrame(stocks, columns=['symbol', 'quantity'])
        holdings = pd.concat([holdings, stks], sort=False)
        grouped_etfs = holdings.groupby(['symbol'], as_index=False)
        aggregated_holdings = grouped_etfs.sum()
        return aggregated_holdings

    def add_prices(self, holdings):
        symbols = holdings['symbol']
        t = Ticker(symbols)
        ticks = t.price
        prices = []
        show_prices = pd.DataFrame.from_dict(ticks, orient='index')
        show_prices.reset_index(level=0, inplace=True)
        show_prices.columns = ['symbol', 'value']
        show_prices = show_prices[show_prices.symbol != '']
        show_prices = show_prices[~show_prices.value.str.contains('Quote not found for ticker symbol:', na=False)]
        df = pd.DataFrame.from_records(show_prices['value'].to_list())
        prices = df[['symbol', 'regularMarketPrice']]
        holdings = holdings.set_index('symbol')
        prices = prices.set_index('symbol')
        holdings = holdings.join(prices['regularMarketPrice'])
        holdings['market_value'] = holdings['quantity'] * holdings['regularMarketPrice']
        return sort_prices(holdings)
