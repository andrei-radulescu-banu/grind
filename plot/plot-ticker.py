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
    world_trading_data = 'world_trading_data'

    def __str__(self):
        return self.value

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot data history.')
    parser.add_argument('-t', '--ticker', nargs='+', help='Ticker')
    parser.add_argument('--dir', default=DirDefault, help='Market data directory. Default: {}.'.format(DirDefault))
    parser.add_argument('-i', '--interface', default=InterfaceDefault, type=DownloadInterface, choices=list(DownloadInterface), help='Download interface. Default: {}.'.format(InterfaceDefault))
    parser.add_argument('-d', '--debug', action='store_true', help='Enable debug messages.')

    args = parser.parse_args()

    slug = 'yahoo'
    if str(args.interface) == 'alpha_vantage':
        slug = 'alpha-vantage'
    if str(args.interface) == 'world_trading_data':
        slug = 'world-trading-data'

    dirname = '{}/stocks/{}'.format(DirDefault, slug)

    files = [f for f in os.listdir(dirname)]

    for ticker in args.ticker:
        matching = [f for f in files if '{}_'.format(ticker) in f]
        if not matching:
            if args.debug:
                print('No data for {}'.format(ticker))
                continue
