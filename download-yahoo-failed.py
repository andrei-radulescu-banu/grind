#!/usr/bin/env python

import sys, os
import pandas as pd
import numpy as np
import argparse
import datetime
from enum import Enum

# Local modules
import worldtradingdata as wtd

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

    ticker_yahoo_failed = ['PMCS', 'ADCT', 'PMTC', 'NOVL', 'GAS.2', 'RSHCQ', 'DJ', 'CCTYQ', 'AW', 'WEN.2', 'UNS1', 'MIL.', 'BMS', 'TE', 'RDC', 'NVLS', 'JNS', 'FDO', 'FNP', 'DG.1', 'HMA', 'SIAL', 'BFB', 'APCC.', 'HSP', 'MWV', 'APOL', 'DF', 'MWW', 'CBG', 'TMK', 'AV.1', 'WYN', 'H.4', 'WFM', 'NSM.2', 'WIN', 'LXK', 'EKDKQ', 'CBSS', 'ASD', 'BCR', 'BJS', 'LLTC', 'UST.1', 'ABKFQ', 'SNDK', 'LTD', 'LLL', 'BMET', 'CITGQ', 'RAI', 'KMI.1', 'AMZN', 'PGN', 'STJ', 'QWST', 'SHLD', 'EDS.', 'WFT', 'BRCM', 'SWY', 'COH', 'MHS', 'FRX', 'GENZ', 'EOP', 'XTO', 'MTLQQ', 'CCU.1', 'JAVA', 'BSC.1', 'DTV', 'SPLS', 'FDC', 'SYMC', 'APC', 'AT.', 'MHFI', 'TXU', 'BNI', 'YHOO', 'BUD.2', 'LEHMQ', 'WAG', 'MOT', 'TYC', 'WYE', '0R01', 'DYNIQ', 'HCBK', 'ESV', 'KFT', 'TSO', 'LUK', 'ACAS', 'GGP', 'TYC', 'LO', 'TSS', 'CAM', 'HCP', 'CEPH', 'HRS', 'DPS', 'DV', 'HCN', 'NU', 'PCS', 'TWC', 'DTV', 'PCLN', 'MJN', 'RHT', 'CFN', 'ARG', 'CVC', 'TYC', 'JOY', 'ANRZQ', 'OSHWQ', 'OSHSQ', 'RDC', 'DTV', 'KRFT', 'ESV', 'PETM', 'KORS', 'GGP', 'WIN', 'TWC', 'GMCR', 'MHFI', 'TYC', 'LVLT', 'HCA', 'BLD WI', 'CC WI', 'BXLT', 'CPGX', 'GGP', 'LLL', 'DWDP', 'NLOK', 'GL']

    ticker_fail = []
    ticker_success = []
    
    for ticker in ticker_yahoo_failed:
        if args.debug:
            print('Downloading {} from worldtradingdata'.format(ticker))
        ret = wtd.download_hist_world_trading_data(ticker, force=args.force, debug=args.debug)
        if ret:
            ticker_success.append(ticker)
        else:
            ticker_fail.append(ticker)
                
    if args.debug:
        print('{} symbols success, {} symbols fail ({})'.format(len(ticker_success), len(ticker_fail), ticker_fail))
            
