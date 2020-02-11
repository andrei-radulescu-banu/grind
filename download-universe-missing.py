#!/usr/bin/env python

import sys, os
import yfinance as yf
import pandas as pd
import numpy as np
import argparse
import datetime
from enum import Enum

# Local modules
import yahoo
import alphavantage as av
import worldtradingdata as wtd

DirDefault = '/home/andrei/src/market-data'
SecuritiesDefault = 'securities.csv'
InterfaceDefault = 'world_trading_data'

class DownloadInterface(Enum):
    alpha_vantage = 'alpha_vantage'
    quandl = 'quandl'
    yahoo = 'yahoo'
    world_trading_data = 'world_trading_data'

    def __str__(self):
        return self.value

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download universe history.')
    parser.add_argument('-s', '--securities-file', default=SecuritiesDefault, help='Securities universe. Default: {}'.format(SecuritiesDefault))
    parser.add_argument('--dir', default=DirDefault, help='Market data directory. Default: {}.'.format(DirDefault))
    parser.add_argument('-i', '--interface', default=InterfaceDefault, type=DownloadInterface, choices=list(DownloadInterface), help='Download interface. Default: {}.'.format(InterfaceDefault))
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug messages.')
    parser.add_argument('-f', '--force', action='store_true', help='Force a download even if the data is cached.')

    args = parser.parse_args()

    date = datetime.date.today()
    date_str = date.strftime('%Y%m%d')

    fname = '{}/{}'.format(DirDefault, SecuritiesDefault)
    securities_df = pd.read_csv(fname)
    if args.debug:
        print('Loaded {}'.format(fname))
    #print(securities_df)

    slug = 'yahoo'
    if str(args.interface) == 'alpha_vantage':
        slug = 'alpha-vantage'
    if str(args.interface) == 'world_trading_data':
        slug = 'world-trading-data'

    dirname = '{}/stocks/{}'.format(DirDefault, slug)
    
    files = [f for f in os.listdir(dirname)]
    
    ticker_fail = []
    ticker_success = []
    
    for index, row in securities_df.iterrows():
        matching = [f for f in files if '{}_'.format(row['Ticker']) in f]
        if matching:
            if args.debug:
                print('Already have {}'.format(matching))
                continue
        
        if args.debug:
            print('Downloading {} from {}'.format(row['Ticker'], args.interface))
        if str(args.interface) == 'yahoo':    
            ret = yahoo.download_hist_yahoo(row['Ticker'], ISIN=row['ISIN'], force=args.force, debug=args.debug)
            if ret:
                ticker_success.append(row['Ticker'])
            else:
                ticker_fail.append(row['Ticker'])

        if str(args.interface) == 'alpha_vantage':
            ret = av.download_hist_alpha_vantage(row['Ticker'], ISIN=row['ISIN'], force=args.force, debug=args.debug)
            if ret:
                ticker_success.append(row['Ticker'])
            else:
                ticker_fail.append(row['Ticker'])

        if str(args.interface) == 'world_trading_data':
            ret = wtd.download_hist_world_trading_data(row['Ticker'], ISIN=row['ISIN'], force=args.force, debug=args.debug)
            if ret:
                ticker_success.append(row['Ticker'])
            else:
                ticker_fail.append(row['Ticker'])
                
    if args.debug:
        print('{} symbols success, {} symbols fail ({})'.format(len(ticker_success), len(ticker_fail), ticker_fail))            
