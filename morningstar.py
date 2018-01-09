import sys
import requests
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

    # Table name is the ticker
    df.index.name = ticker.upper()

    return df

def fund_trailing_total_returns(ticker):
    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = web.get_web_page_table(url + ticker, False, 14)

    # Table name is the ticker
    df.index.name = ticker.upper()

    return df 

def fund_historical_quarterly_returns(ticker):
    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = web.get_web_page_table(url + ticker, False, 16)

    # Table name is the ticker
    df.index.name = ticker.upper()

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
