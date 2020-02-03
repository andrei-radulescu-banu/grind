#!/usr/bin/env python

import sys, os
import argparse

Url = 'https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf/1467271812596.ajax?fileType=csv&fileName=IVV_holdings&dataType=fund&asOfDate='
Data_Top = '{}/data/'.format(os.path.realpath(__file__))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download S&P500 IVV ETF Universe.')
    parser.add_argument('--url', default=Url, help='Base URL. Default: {}'.format(Url))
    parser.add_argument('-d', '--date', default='', help='Date in YYYYMMDD format.')
    parser.add_argument('-t', '--top', default=Data_Top, help='Where to save the data. Default: {}'.format(Data_Top))

    args = parser.parse_args()
    args.func(args)
