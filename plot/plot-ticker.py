#!/usr/bin/env python

import sys, os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import datetime
from enum import Enum

DirDefault = '/home/andrei/src/market-data'
InterfaceDefault = 'world_trading_data'

class DownloadInterface(Enum):
    alpha_vantage = 'alpha_vantage'
    quandl = 'quandl'
    yahoo = 'yahoo'
    stooq = 'stooq'
    world_trading_data = 'world_trading_data'

    def __str__(self):
        return self.value

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot data history.')
    parser.add_argument('-t', '--ticker', help='Ticker', required=True)
    parser.add_argument('--dir', default=DirDefault, help='Market data directory. Default: {}.'.format(DirDefault))
    parser.add_argument('-i', '--interface', nargs='*', default=[InterfaceDefault], type=DownloadInterface, choices=list(DownloadInterface), help='Download interface. Default: {}.'.format(InterfaceDefault))
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug messages.')

    args = parser.parse_args()

    # gca stands for 'get current axis'
    ax = plt.gca()

    for interface in args.interface:

        slug = 'yahoo'
        if str(interface) == 'alpha_vantage':
            slug = 'alpha-vantage'
        if str(interface) == 'world_trading_data':
            slug = 'world-trading-data'

        dirname = '{}/stocks/{}'.format(DirDefault, slug)

        files = [f for f in os.listdir(dirname)]

        matching = [str(f) for f in files if '{}_'.format(args.ticker) in f]
        if not matching:
            if args.debug:
                print('No data for {}'.format(args.ticker))
                continue

        matching.sort(reverse=True)
            
        df = pd.read_csv('{}/{}'.format(dirname, matching[0]))
        if df.empty:
            if args.debug:
                print('No data for {}'.format(args.ticker))
            continue
        df.plot(kind='line',x='Date',y='Close',label=interface,ax=ax)

    plt.legend(loc='best')
    plt.show()
