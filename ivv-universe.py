#!/usr/bin/env python

import sys, os
import argparse
import datetime
import glob
import numpy as np
import pandas as pd

DirDefault = '/home/andrei/src/market-data/ivv'
OutputDefault = 'securities.csv'

if __name__ == "__main__":    
    parser = argparse.ArgumentParser(description='Generate S&P500 Universe based on IVV ETF.')
    parser.add_argument('--dir', default=DirDefault, help='Directory of IVV csv files. Default: {}.'.format(DirDefault))
    parser.add_argument('--output', default=DirDefault, help='Directory of IVV csv files. Default: {}.'.format(DirDefault))

    args = parser.parse_args()

    ivv_fnames = glob.glob('{}/IVV_holdings_*.csv'.format(args.dir))

    securities_df = pd.DataFrame(columns = ['Ticker', 'Name', 'Sector', 'SEDOL', 'ISIN', 'DateIn', 'DateOut'])
    
    for ivv_fname in ivv_fnames:
        print(ivv_fname)
        df = pd.read_csv(ivv_fname, delimiter = ',', skiprows=9)
        for index, row in df.iterrows():
            # Check if securities_df contains ISIN
            # Reference: https://stackoverflow.com/questions/21319929/how-to-determine-whether-a-pandas-column-contains-a-particular-value            
            if row['ISIN'] not in securities_df['ISIN'].values:
                securities_df = securities_df.append({'Ticker':row['Ticker'], 'Name':row['Name'], 'Sector':row['Sector'], 'SEDOL':row['SEDOL'], 'ISIN':row['ISIN'], 'DateIn': 0},ignore_index=True)
                
        break

    print(securities_df)
