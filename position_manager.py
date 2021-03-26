import portfolio_analyzer as pa

class PortfolioManager:
    def get_expanded_symbols(self):
        best_prices = self.get_sorted_portfolio()
        return best_prices['symbol']


    def get_sorted_portfolio(self):
        p = pa.PositionAnalyzer()
        weighted_holdings = p.get_aggregated_holdings(p.etfs, p.stocks)
        priced = p.add_prices(weighted_holdings)
        priced.reset_index(level=0, inplace=True)
        return priced[~priced.symbol.str.contains('.KS', na=False)]

    def export_portfolio(self, portfolio, fileName):
        portfolio.to_csv(fileName)


#priced.to_csv('porfolio.csv')

