#!/usr/bin/env python

import sys, os
import pandas as pd
import argparse
import datetime
import requests

DirDefault = '/home/andrei/src/market-data/stocks/quandl'

def download_hist_quandl(ticker, ISIN=None, dirname=DirDefault, force=False, debug=False):
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

    api_key = os.getenv('QUANDL_API_KEY')
    if not api_key:
        print('QUANDL_API_KEY environment variable not set up')
        return False
    
    url = 'https://www.quandl.com/api/v3/datasets/WIKI/{}.csv?api_key={}'.format(ticker, api_key)
    if debug:
        print('Get {} from {}'.format(ticker, url))

    r = requests.get(url, timeout=10)

    if r.status_code != 200:
        if debug:
            print('HTTP status code {}'.format(r.status_code))
        return False

    content = r.content
    
    with open(fname, "wb") as f:
        f.write(content)
        
    if debug:
        print('Saved {}'.format(fname))

    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Quandl data.')
    parser.add_argument('-t', '--ticker', nargs='+', help='Ticker')
    parser.add_argument('--dir', default=DirDefault, help='Output directory. Default: {}.'.format(DirDefault))
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug messages.')
    parser.add_argument('-f', '--force', action='store_true', help='Force a download even if the data is cached.')

    args = parser.parse_args()

    for ticker in args.ticker:
        download_hist_quandl(ticker,
                             dirname=args.dir,
                             force=args.force,
                             debug=args.debug)    
