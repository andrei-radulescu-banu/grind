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
    parser.add_argument('-f', '--force', action='store_true', help='Force a download even if the data is cached.')

    args = parser.parse_args()

    date = datetime.date.today()
    date_str = date.strftime("%Y%m%d")
    
    for ticker in args.ticker:
        # Will be saving the data in this file name
        fname = '{}/{}_{}.csv'.format(args.dir, ticker, date_str)

        # Check for old data
        if not args.force:
            if os.path.exists(fname):
                if args.debug:
                    print('{} already available'.format(fname))
                    continue

        # Remove old data
        if os.path.exists(fname):
            os.unlink(fname)

        # Create the yf ticker object
        yticker = yf.Ticker(ticker)

        # Download the max history
        df = yticker.history(period="max")

        # Check if we downloaded anything
        if df.empty:
            continue

        # Save to file
        df.to_csv(fname)
        
        if args.debug:
            print('Saved {}'.format(fname))
    
