#!/usr/bin/env python

import sys, os
import argparse
from datetime import datetime

Url = 'https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf/1467271812596.ajax?fileType=csv&fileName=IVV_holdings&dataType=fund&asOfDate='
Date = datetime.today().strftime('%Y%m%d')
Data_Top = '{}/data/'.format(os.path.realpath(__file__))

if __name__ == "__main__":
    global Url
    global Data_Top
    
    parser = argparse.ArgumentParser(description='Download S&P500 IVV ETF Universe.')
    parser.add_argument('--url', default=Url, help='Base URL. Default: {}.'.format(Url))
    parser.add_argument('-d', '--date', default=Date, help='Date in YYYYMMDD format. Default: {}'.format(Date))
    parser.add_argument('-t', '--top', default=Data_Top, help='Where to save the data. Default: {}'.format(Data_Top))
    parser.add_argument('-a', '--all', action='store_true', help='Download all preceding dates.')
    parser.add_argument('-f', '--force', action='store_true', help='Overwrite old data, if already downloaded.')

    args = parser.parse_args()
    args.func(args)
    
