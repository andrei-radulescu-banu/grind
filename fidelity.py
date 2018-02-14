#!/usr/bin/env python

import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
from tickerscrape import web
import argparse
import unidecode

"""
Module for parsing Morningstar web data.
"""

_ticker_cache = dict()
_name_cache = dict()

def ticker_type(ticker):
    """
    Description:
    The Morningstar URL for getting quotes for cefs, etfs, funds, indexes, stocks

    Parameters:
    ticker - The security ticker.

    Returns:
    A string with value "Cash", "CEF", "ETF", "Index", "Mutual Fund", "Stock"
    (or "" in case the ticker is neither)
    """

    # Special case for cash
    if ticker.lower() == "cash":
        return "Cash"

    if ticker not in _ticker_cache:
        # The Morningstar URL for funds
        url = "http://quote.morningstar.com/Quote/Quote.aspx?ticker="
    
        # Get the page
        r = requests.get(url + ticker, allow_redirects = False)
   
        # Enable to inspect headers
        #print(r)
        #print(r.headers)

        if r.status_code == 302:
            if "/stock/" in r.headers['Location']:
                _ticker_cache[ticker] = "Stock"
            elif "/fund/" in r.headers['Location']:
                _ticker_cache[ticker] = "Mutual Fund"
            elif "//etfs." in r.headers['Location']:
                _ticker_cache[ticker] = "ETF"
                return("ETF")
            elif "//cef." in r.headers['Location']:
                _ticker_cache[ticker] = "CEF"
            elif "/indexquote/" in r.headers['Location']:
                _ticker_cache[ticker] = "Index"
            
    if ticker in _ticker_cache:
        return(_ticker_cache[ticker])
    
    return ""

def ticker_name(ticker):
    """
    Description:
    Get ETF, fund or stock name

    Parameters:
    ticker - The etf, fund, stock ticker.

    Returns:
    The ticker name, "" (in case the ticker can't be resolved)
    """

    if ticker in _name_cache:
        return(_name_cache[ticker])

    # Should not contain spaces
    if " " in ticker:
        return None

    # Ticker check    
    tt = ticker_type(ticker)

    name = None
    if tt == "CEF" or tt == "ETF" or tt == "Index" or tt == "Mutual Fund":
        name = fund_name(ticker)
    
    if tt == "Stock":
        name = stock_name(ticker)
    
    if name is not None:
        _name_cache[ticker] = name

    return name


def _parse_ticker_type_f(args):
    type = ticker_type(args.ticker)

    if type != "":
        print(type)

def _parse_ticker_name_f(args):
    type = ticker_name(args.ticker)

    if type != "":
        print(type)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Fidelity data.')

    # Subparsers
    subparsers = parser.add_subparsers(help='Sub-command help')

    parser_ticker_type = subparsers.add_parser('ticker-type', help='Get ticker type (cef, etf, index, fund, stock, cash)')
    parser_ticker_type.add_argument('ticker', help='Ticker')
    parser_ticker_type.set_defaults(func=_parse_ticker_type_f)

    parser_ticker_name = subparsers.add_parser('ticker-name', help='Get name (all)')
    parser_ticker_name.add_argument('ticker', help='Ticker')
    parser_ticker_name.set_defaults(func=_parse_ticker_name_f)

    args = parser.parse_args()
    args.func(args)
