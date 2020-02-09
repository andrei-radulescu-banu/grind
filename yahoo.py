#!/usr/bin/env python

import sys, os
import yfinance as yf
import pandas as pd
import argparse
import datetime

DirDefault = '/home/andrei/src/market-data/stocks'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Yahoo data.')
    parser.add_argument('-t', '--ticker', nargs='+', help='Ticker')
    parser.add_argument('--dir', default=DirDefault, help='Directory of IVV csv files. Default: {}.'.format(DirDefault))
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug messages.')

    args = parser.parse_args()

    date = datetime.date.today()
    date_str = date.strftime("%Y%m%d")
    
    for ticker in args.ticker:
        fname = '{}/{}_{}.csv'.format(args.dir, ticker, date_str)
        print(fname)
        #        yticker = yf.Ticker(ticker)

    
