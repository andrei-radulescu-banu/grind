#!/usr/bin/env python

import sys, os
import argparse
import datetime
import pandas
import numpy as np

DirDefault = '/home/andrei/src/market-data/ivv'

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description='Generate S&P500 Universe based on IVV ETF.')
    parser.add_argument('--dir', default=DirDefault, help='Directory of IVV csv files. Default: {}.'.format(DirDefault))

    args = parser.parse_args()

