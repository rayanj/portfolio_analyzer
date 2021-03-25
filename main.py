import position_manager as pm

manager = pm.PortfolioManager()
symbols = manager.get_expanded_symbols()
print(symbols)