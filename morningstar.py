import sys
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
from tickerscrape import web
import argparse
import unidecode

"""
Module for parsing Morningstar web data.
"""

def fund_performance_history(ticker):
    """
    Get fund performance history.
    
    Parameters:
    ticket - The fund ticker

    Returs: DataFrame with the performance history. 
    Run 'morningstar.py pfh ticker' to see the result format.
    """
    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = web.get_web_page_table(url + ticker, False, 12)

    # Trim last three rows
    df.drop(df.tail(3).index,inplace=True)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df

def fund_performance_history2(ticker):
    # The Morningstar URL for funds
    url = "http://performance.morningstar.com/Performance/fund/performance-history-1.action?&ops=clear&t="
    
    df = web.get_web_page_table(url + ticker, False, 0)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    # Fix the unprintable unicode characters
    df.index.name = unidecode.unidecode(df.index.name)
    df1 = df.applymap(lambda x: unidecode.unidecode(x))

    return df1

def fund_trailing_total_returns(ticker):
    # The Morningstar URL for funds
    url = "http://performance.morningstar.com/Performance/fund/trailing-total-returns.action?t="    

    df = web.get_web_page_table(url + ticker, False, 0)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    # Fix the unprintable unicode characters
    df.index.name = unidecode.unidecode(df.index.name)
    df1 = df.applymap(lambda x: unidecode.unidecode(x))

    return df1 

def fund_trailing_total_returns2(ticker):
    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = web.get_web_page_table(url + ticker, False, 14)
    df.iloc[0, 1] = "Total Return %"
    df.iloc[0, 2] = unidecode.unidecode(df.iloc[0, 2]).replace("\r", "").replace("\n", "")
    df.iloc[0, 3] = unidecode.unidecode(df.iloc[0, 3]).replace("\r", "").replace("\n", "")
    df.iloc[0, 4] = "% Rank in Cat"

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df 

def stock_price(ticker):
    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = web.get_web_page_table(url + ticker, False, 14)
    df.iloc[0, 1] = "Total Return %"
    df.iloc[0, 2] = unidecode.unidecode(df.iloc[0, 2]).replace("\r", "").replace("\n", "")
    df.iloc[0, 3] = unidecode.unidecode(df.iloc[0, 3]).replace("\r", "").replace("\n", "")
    df.iloc[0, 4] = "% Rank in Cat"

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df 

def fund_price(ticker):
    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = web.get_web_page_table(url + ticker, False, 14)
    df.iloc[0, 1] = "Total Return %"
    df.iloc[0, 2] = unidecode.unidecode(df.iloc[0, 2]).replace("\r", "").replace("\n", "")
    df.iloc[0, 3] = unidecode.unidecode(df.iloc[0, 3]).replace("\r", "").replace("\n", "")
    df.iloc[0, 4] = "% Rank in Cat"

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df 

def fund_historical_quarterly_returns(ticker, years = 5, frequency = "m"):
    """
    Parameters:
    ticker - the fund or ETF ticker
    years - the number of years. Default: 5.
    frequency - "q" for quarterly, "m" for monthly. Default: "q"
    """
    # The Morningstar URL for funds
    url = "http://performance.morningstar.com/Performance/fund/historical-returns.action?&ops=clear&y=%s&freq=%s&t=" % (years, frequency)
    
    df = web.get_web_page_table(url + ticker, False, 0)

    df.fillna(value="", inplace=True)
    df1 = df.drop(df.columns[[3, 4, 5, 6, 7]], axis=1)
    df = df1

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df 

def fund_historical_quarterly_returns2(ticker):
    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = web.get_web_page_table(url + ticker, False, 16)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df 

def stock_price(ticker):
    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = web.get_web_page_table(url + ticker, False, 16)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df 

def net_asset_value(ticker):
    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = web.get_web_page_table(url + ticker, False, 16)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df 

def parse_pfh_f(args):
    df = fund_performance_history(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def parse_pfh2_f(args):
    df = fund_performance_history2(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def parse_ttl_f(args):
    df = fund_trailing_total_returns(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def parse_ttl2_f(args):
    df = fund_trailing_total_returns2(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def parse_qtr_f(args):
    df = fund_historical_quarterly_returns(args.ticker, args.years, args.frequency)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def parse_qtr2_f(args):
    df = fund_historical_quarterly_returns2(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def parse_sp(args):
    df = stock_price(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def parse_nav(args):
    df = net_asset_value(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Morningstar data.')

    # Subparsers
    subparsers = parser.add_subparsers(help='Sub-command help')

    parser_pfh = subparsers.add_parser('pfh', help='Performace history')
    parser_pfh.add_argument('ticker', help='Ticker')
    parser_pfh.set_defaults(func=parse_pfh_f)

    parser_pfh2 = subparsers.add_parser('pfh2', help='Performace history 2')
    parser_pfh2.add_argument('ticker', help='Ticker')
    parser_pfh2.set_defaults(func=parse_pfh2_f)

    parser_ttl = subparsers.add_parser('ttl', help='Trailing total returns')
    parser_ttl.add_argument('ticker', help='Ticker')
    parser_ttl.set_defaults(func=parse_ttl_f)

    parser_ttl2 = subparsers.add_parser('ttl2', help='Trailing total returns 2')
    parser_ttl2.add_argument('ticker', help='Ticker')
    parser_ttl2.set_defaults(func=parse_ttl2_f)

    parser_qtr = subparsers.add_parser('qtr', help='Historical quarterly returns')
    parser_qtr.add_argument('ticker', help='Ticker')
    parser_qtr.add_argument('-y', '--years', type=int, default=5, help='Number of years (default 5)')
    parser_qtr.add_argument('-f', '--frequency', default='m', help='Frequency (m=monthly, q=quarterly, default=m)')
    parser_qtr.set_defaults(func=parse_qtr_f)

    parser_qtr2 = subparsers.add_parser('qtr2', help='Historical quarterly returns2')
    parser_qtr2.add_argument('ticker', help='Ticker')
    parser_qtr2.set_defaults(func=parse_qtr2_f)

    parser_sp = subparsers.add_parser('sp', help='Stock price')
    parser_sp.add_argument('ticker', help='Ticker')
    parser_sp.set_defaults(func=parse_sp)

    parser_nav = subparsers.add_parser('nav', help='Mutual fund net asset value')
    parser_nav.add_argument('ticker', help='Ticker')
    parser_nav.set_defaults(func=parse_nav)

    args = parser.parse_args()
    args.func(args)
