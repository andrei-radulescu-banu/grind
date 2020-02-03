#!/usr/bin/env python

import sys
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download S&P500 IVV ETF Universe.')
    parser.add_argument('--url', default='https://www.ishares.com/us/products/239726/ishares-core-sp-500-etf/1467271812596.ajax?fileType=csv&fileName=IVV_holdings&dataType=fund&asOfDate=', help='Base URL. ')
    parser.add_argument('-d', '--date', default='', help='Date in YYYYMMDD format.')

    args = parser.parse_args()
    args.func(args)
