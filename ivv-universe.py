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

    securities_df = pd.DataFrame(columns = ['Ticker', 'Name', 'Sector', 'SEDOL', 'ISIN', 'DateIn', 'DateOut', 'OldTicker'])

    securities = dict()
    
    for ivv_fname in ivv_fnames:
        print(ivv_fname)

        # Extract the date from the csv filename
        date = ivv_fname[ivv_fname.find('IVV_holdings_') + len('IVV_holdings_'):-len('.csv')]
        
        df = pd.read_csv(ivv_fname, delimiter = ',', skiprows=9)
        for index, row in df.iterrows():
            # Skip if not equity
            if row['Asset Class'] != 'Equity':
                continue
            
            # Check if securities_df contains ISIN
            # Reference: https://stackoverflow.com/questions/21319929/how-to-determine-whether-a-pandas-column-contains-a-particular-value            
            if row['ISIN'] not in securities:
                # New security
                securities_df = securities_df.append({'Ticker':row['Ticker'], 'Name':row['Name'], 'Sector':row['Sector'], 'SEDOL':row['SEDOL'], 'ISIN':row['ISIN'], 'DateIn': date},ignore_index=True)
                securities[row['ISIN']] = row['Ticker']
            else:
                # Old security
                idx = securities_df.loc[securities_df['ISIN'] == row['ISIN']].index[0]
                
                if securities[row['ISIN']] != row['Ticker']:
                    print('ISIN {} changed Ticker from {} to {}'.format(row['ISIN'], securities[row['ISIN']], row['Ticker']))
                    securities_df.loc[idx, 'Ticker'] = row['Ticker']
                    securities_df.loc[idx, 'OldTicker'] = "{} {}".format(row['Ticker'], securities_df.loc[idx, 'OldTicker'])

                securities_df.loc[idx, 'Name'] = row['Name']

    print(securities_df)
