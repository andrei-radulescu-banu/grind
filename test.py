import sys
import tickerscrape.fund as f
import pandas as pd
from tabulate import tabulate

if __name__ == "__main__":
    # Executed only if run as a script
    if (len(sys.argv) == 2):
        df = f.morningstar_fund_trailing_total_returns(sys.argv[1])
        print(tabulate(df, headers='keys', tablefmt='psql'))

        df = f.morningstar_fund_performance_history(sys.argv[1])        
        print(tabulate(df, headers='keys', tablefmt='psql'))

        df = f.morningstar_fund_historical_quarterly_returns(sys.argv[1])        
        print(tabulate(df, headers='keys', tablefmt='psql'))
    else:
        print("Usage: %s ticker_symbol" % sys.argv[0])

