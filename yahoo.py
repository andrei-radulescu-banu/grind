#!/usr/bin/env python

import sys, os
import yfinance as yf
import pandas as pd
import argparse
import datetime

DirDefault = '/home/andrei/src/market-data/stocks/yahoo'

def download_hist_yahoo(ticker, ISIN=None, dirname=DirDefault, force=False, debug=False):
    # Today's date
    date = datetime.date.today()
    date_str = date.strftime("%Y%m%d")

    # Will be saving the data in this file name
    fname = '{}/{}_{}.csv'.format(dirname, ticker, date_str)

    # Check for old data
    if not force:
        if os.path.exists(fname):
            if debug:
                print('{} already available'.format(fname))
                return True

    # Remove old data
    if os.path.exists(fname):
        os.unlink(fname)

    # Create the yf ticker object
    yticker = yf.Ticker(ticker)

    # Check the ISIN, if it was passed in
    try:
        if ISIN and ISIN != yticker.isin:
            return False
    except:
        pass

    # Download the max history
    df = yticker.history(period="max")

    # Check if we downloaded anything
    if df.empty:
        return False

    # Save to file
    df.to_csv(fname)
        
    if debug:
        print('Saved {}'.format(fname))

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Yahoo data.')
    parser.add_argument('-t', '--ticker', nargs='+', help='Ticker')
    parser.add_argument('--dir', default=DirDefault, help='Output directory. Default: {}.'.format(DirDefault))
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug messages.')
    parser.add_argument('-f', '--force', action='store_true', help='Force a download even if the data is cached.')

    args = parser.parse_args()

    date = datetime.date.today()
    date_str = date.strftime("%Y%m%d")
    
    for ticker in args.ticker:
        download_hist_yahoo(ticker,
                            dirname=args.dir,
                            force=args.force,
                            debug=args.debug)    
