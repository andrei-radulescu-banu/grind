#!/usr/bin/env python

import sys, os
import yfinance as yf
import pandas as pd
import argparse
import datetime

DirDefault = '/home/andrei/src/market-data'
SecuritiesDefault = 'securities.csv'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download universe history.')
    parser.add_argument('-s', '--securities-file', default=SecuritiesDefault, help='Securities universe. Default: {}'.format(SecuritiesDefault))
    parser.add_argument('--dir', default=DirDefault, help='Market data directory. Default: {}.'.format(DirDefault))
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug messages.')
    parser.add_argument('-f', '--force', action='store_true', help='Force a download even if the data is cached.')

    args = parser.parse_args()

    date = datetime.date.today()
    date_str = date.strftime('%Y%m%d')

    fname = '{}/{}'.format(DirDefault, SecuritiesDefault)
    securities_df = pd.read_csv(fname)
    if args.debug:
        print('Loaded {}'.format(fname))
    print(securities_df)
