import sys
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
from tickerscrape import web

def fund_performance_history(ticker):
    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = web.get_web_page_table(url + ticker, False, 12)

    # Trim last three rows
    df.drop(df.tail(3).index,inplace=True)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df

def fund_trailing_total_returns(ticker):
    # The Morningstar URL for funds
    url = "http://performance.morningstar.com/Performance/fund/trailing-total-returns.action?t="    

    df = web.get_web_page_table(url + ticker, False, 0)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df 

def fund_trailing_total_returns2(ticker):
    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = web.get_web_page_table(url + ticker, False, 14)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df 

def fund_historical_quarterly_returns(ticker):
    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = web.get_web_page_table(url + ticker, False, 16)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df 

if __name__ == "__main__":
    # execute only if run as a script
    if (len(sys.argv) == 2):
        #df = morningstar_fund_trailing_total_returns(sys.argv[1])
        #print(tabulate(df, headers='keys', tablefmt='psql'))

        #df = morningstar_fund_performance_history(sys.argv[1])        
        #print(tabulate(df, headers='keys', tablefmt='psql'))

        df = morningstar_fund_historical_quarterly_returns(sys.argv[1])        
        print(tabulate(df, headers='keys', tablefmt='psql'))
    else:
        print("Usage: %s ticker_symbol" % sys.argv[0])
