import sys
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate
from tickerscrape import web
import argparse
import unidecode

"""
Module for parsing Morningstar web data.
"""

def fund_performance_history(ticker):
    """
    Description:
    Get etf or fund performance history. Does not work for stocks.
    
    Parameters:
    ticker - The etf or fund ticker.

    Returs: 
    DataFrame with the performance history. 
    Run 'morningstar.py pfh ticker' to see the result format.
    """
    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = web.get_web_page_table(url + ticker, False, 12)

    # Trim last three rows
    df.drop(df.tail(3).index,inplace=True)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df

def fund_performance_history2(ticker):
    """
    Description:
    Get etf or fund performance history. Does not work for stocks.
    
    Parameters:
    ticker - The etf or fund ticker.

    Returs: 
    DataFrame with the performance history. 
    Run 'morningstar.py pfh2 ticker' to see the result format.
    """
    # The Morningstar URL for funds
    url = "http://performance.morningstar.com/Performance/fund/performance-history-1.action?&ops=clear&t="
    
    df = web.get_web_page_table(url + ticker, False, 0)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    # Fix the unprintable unicode characters
    df.index.name = unidecode.unidecode(df.index.name)
    df1 = df.applymap(lambda x: unidecode.unidecode(x))
    df = df1

    return df

def trailing_total_returns(ticker):
    """
    Description:
    Get trailing total returns. 
    
    Parameters:
    ticker - The ticker.

    Returs: 
    DataFrame with the trailing total returns.
    Run 'morningstar.py ttl ticker' to see the result format.
    """
    # The Morningstar URL for funds
    url = "http://performance.morningstar.com/Performance/fund/trailing-total-returns.action?t="    

    df = web.get_web_page_table(url + ticker, False, 0)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    # Fix the unprintable unicode characters
    df.index.name = unidecode.unidecode(df.index.name)
    df1 = df.applymap(lambda x: unidecode.unidecode(x))

    return df1 

def fund_trailing_total_returns2(ticker):
    """
    Description:

    Parameters:
    ticker - The fund ticker

    Returns:

    """
    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = web.get_web_page_table(url + ticker, False, 14)
    df.iloc[0, 1] = "Total Return %"
    df.iloc[0, 2] = unidecode.unidecode(df.iloc[0, 2]).replace("\r", "").replace("\n", "")
    df.iloc[0, 3] = unidecode.unidecode(df.iloc[0, 3]).replace("\r", "").replace("\n", "")
    df.iloc[0, 4] = "% Rank in Cat"

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df 

def historical_quarterly_returns(ticker, years = 5, frequency = "m"):
    """
    Description:
    Get historical quarterly returns.

    Parameters:
    ticker - The etf, fund or stock ticker.
    years - The number of years. Default: 5.
    frequency - "q" for quarterly, "m" for monthly. Default: "q"
    """
    # The Morningstar URL for funds
    url = "http://performance.morningstar.com/Performance/fund/historical-returns.action?&ops=clear&y=%s&freq=%s&t=" % (years, frequency)
    
    df = web.get_web_page_table(url + ticker, False, 0)

    df.fillna(value="", inplace=True)
    df1 = df.drop(df.columns[[3, 4, 5, 6, 7]], axis=1)
    df = df1

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df 

def fund_historical_quarterly_returns(ticker):
    """
    Description:
    Get historical quarterly returns for etfs and funds. 
    Does not work with stocks.

    Parameters:
    ticker - the etf or fund ticker

    Returns:

    """
    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = web.get_web_page_table(url + ticker, False, 16)

    # Promote 1st row and column as labels
    df = web.dataframe_promote_1st_row_and_column_as_labels(df)

    return df 

def stock_price(ticker):
    """
    Description:
    Get the etf or stock quote, and other related data.

    Parameters:
    ticker - The etf or stock ticker.

    Returns:

    """
    # The Morningstar URL for funds
    url = "http://quotes.morningstar.com/stock/c-header?&t=" + ticker
    
    # Get the page
    web_page = web.get_web_page(url, False)

    # Parse the contents
    soup = BeautifulSoup(web_page, 'lxml')

    df = pd.DataFrame(columns = range(1), 
                      index = range(18))
    
    # Set the index
    df['new_index'] = None
    df['new_index'][0] = soup.find("h3", {"gkey": "LastPrice"}).getText().strip()
    df['new_index'][1] = soup.find("h3", {"gkey": "DayChange"}).getText().strip()
    df['new_index'][2] = "Day Change %"
    df['new_index'][3] = soup.find("span", {"gkey": "AferHourLab"}).getText().strip()
    df['new_index'][4] = "After Hours Change"
    df['new_index'][5] = "After Hours Change %"
    df['new_index'][6] = soup.find("span", {"gkey": "AsOf"}).getText().strip()
    df['new_index'][7] = soup.find("h3", {"gkey": "OpenPrice"}).getText().strip()
    df['new_index'][8] = soup.find("h3", {"gkey": "DayRange"}).getText().strip()
    df['new_index'][9] = soup.find("h3", {"gkey": "_52Week"}).getText().strip()
    df['new_index'][10] = soup.find("h3", {"gkey": "ProjectedYield"}).getText().strip()
    df['new_index'][11] = soup.find("h3", {"gkey": "MarketCap"}).getText().strip()
    df['new_index'][12] = soup.find("h3", {"gkey": "Volume"}).getText().strip()
    df['new_index'][13] = soup.find("h3", {"gkey": "AverageVolume"}).getText().strip()
    df['new_index'][14] = soup.find("span", {"gkey": "PE"}).getText().strip()
    df['new_index'][15] = soup.find("h3", {"gkey": "PB"}).getText().strip()
    df['new_index'][16] = soup.find("h3", {"gkey": "PS"}).getText().strip()
    df['new_index'][17] = soup.find("h3", {"gkey": "PC"}).getText().strip()

    # Promote the 'new_index' column as the new index
    df2 = df.set_index('new_index')
    df = df2

    # Clear the index name
    df.index.name = ""

    # Set the ticker name as column label
    df.columns = [ticker.upper()]

    df.iloc[0, 0] = soup.find("div", {"vkey": "LastPrice"}).getText().strip()
    df.iloc[1, 0] = soup.find("div", {"vkey": "DayChange"}).getText().split("|")[0].strip()
    df.iloc[2, 0] = soup.find("div", {"vkey": "DayChange"}).getText().split("|")[1].strip()
    df.iloc[3, 0] = soup.find("span", {"id": "after-hours"}).getText().strip()
    df.iloc[4, 0] = soup.find("span", {"id": "after-daychange-value"}).getText().strip()
    df.iloc[5, 0] = soup.find("span", {"id": "after-daychange-per"}).getText().strip()
    df.iloc[6, 0] = soup.find("span", {"id": "asOfDate"}).getText().strip() + " " + soup.find("span", {"id": "timezone"}).getText().strip()
    df.iloc[7, 0] = soup.find("span", {"vkey": "OpenPrice"}).getText().strip()
    df.iloc[8, 0] = soup.find("span", {"vkey": "DayRange"}).getText().strip()
    df.iloc[9, 0] = soup.find("span", {"vkey": "_52Week"}).getText().strip()
    df.iloc[10, 0] = soup.find("span", {"vkey": "ProjectedYield"}).getText().strip()
    df.iloc[11, 0] = soup.find("span", {"id": "MarketCap"}).getText().strip()
    df.iloc[12, 0] = soup.find("span", {"vkey": "Volume"}).getText().strip()
    df.iloc[13, 0] = soup.find("span", {"vkey": "AverageVolume"}).getText().strip()
    df.iloc[14, 0] = soup.find("span", {"vkey": "PE"}).getText().strip()
    df.iloc[15, 0] = soup.find("span", {"vkey": "PB"}).getText().strip()
    df.iloc[16, 0] = soup.find("span", {"vkey": "PS"}).getText().strip()
    df.iloc[17, 0] = soup.find("span", {"vkey": "PC"}).getText().strip()

    # Fix the unprintable unicode characters
    df1 = df.applymap(lambda x: unidecode.unidecode(x))
    df = df1

    return df

def net_asset_value(ticker):
    """
    Description:
    Get the fund net asset value, and other related data.

    Parameters:
    ticker - The fund ticker.

    Returns:

    """
    # The Morningstar URL for funds
    url = "http://quotes.morningstar.com/fund/c-header?&t=" + ticker
    
    # Get the page
    web_page = web.get_web_page(url, False)

    # Parse the contents
    soup = BeautifulSoup(web_page, 'lxml')

    df = pd.DataFrame(columns = range(1), 
                      index = range(15))
    
    # Set the index
    df['new_index'] = None
    df['new_index'][0] = soup.find("h3", {"gkey": "NAV"}).getText().strip()
    df['new_index'][1] = soup.find("h3", {"gkey": "NavChange"}).getText().strip() + " %"
    df['new_index'][2] = soup.find("span", {"gkey": "AsOf"}).getText().strip()
    df['new_index'][3] = soup.find("span", {"gkey": "OneDayReturnAsOf"}).getText().strip()
    df['new_index'][4] = soup.find("h3", {"gkey": "ttmYield"}).getText().strip()
    df['new_index'][5] = soup.find("h3", {"gkey": "Load"}).getText().strip()
    df['new_index'][6] = soup.find("h3", {"gkey": "TotalAssets"}).getText().strip()
    df['new_index'][7] = soup.find("a", {"gkey": "ExpenseRatio"}).getText().strip()
    df['new_index'][8] = soup.find("a", {"gkey": "FeeLevel"}).getText().strip()
    df['new_index'][9] = soup.find("h3", {"gkey": "Turnover"}).getText().strip()
    df['new_index'][10] = soup.find("h3", {"gkey": "Status"}).getText().strip()
    df['new_index'][11] = soup.find("h3", {"gkey": "MinInvestment"}).getText().strip()
    df['new_index'][12] = soup.find("h3", {"gkey": "Yield"}).getText().strip()
    df['new_index'][13] = soup.find("h3", {"gkey": "MorningstarCategory"}).getText().strip()
    df['new_index'][14] = soup.find("h3", {"gkey": "InvestmentStyle"}).getText().strip()

    # Promote the 'new_index' column as the new index
    df2 = df.set_index('new_index')
    df = df2

    # Clear the index name
    df.index.name = ""

    # Set the ticker name as column label
    df.columns = [ticker.upper()]

    df.iloc[0, 0] = soup.find("span", {"vkey": "NAV"}).getText().strip()
    df.iloc[1, 0] = soup.find("div", {"vkey": "DayChange"}).getText().strip()
    df.iloc[2, 0] = soup.find("span", {"id" : "asOfDate", "vkey": "LastDate"}).getText().strip()
    df.iloc[3, 0] = soup.find("span", {"id" : "oneDayReturnAsOfDate", "vkey": "LastDate"}).getText().strip()
    df.iloc[4, 0] = soup.find("span", {"vkey": "ttmYield"}).getText().strip()
    df.iloc[5, 0] = soup.find("span", {"vkey": "Load"}).getText().strip()
    df.iloc[6, 0] = soup.find("span", {"vkey": "TotalAssets"}).getText().strip()
    df.iloc[7, 0] = soup.find("span", {"vkey": "ExpenseRatio"}).getText().strip()
    df.iloc[8, 0] = soup.find("span", {"vkey": "FeeLevel"}).getText().strip()
    df.iloc[9, 0] = soup.find("span", {"vkey": "Turnover"}).getText().strip()
    df.iloc[10, 0] = soup.find("span", {"vkey": "Status"}).getText().strip()
    df.iloc[11, 0] = soup.find("span", {"vkey": "MinInvestment"}).getText().strip()
    df.iloc[12, 0] = soup.find("span", {"vkey": "Yield"}).getText().strip()
    df.iloc[13, 0] = soup.find("span", {"vkey": "MorningstarCategory"}).getText().strip()
    df.iloc[14, 0] = soup.find("span", {"vkey": "InvestmentStyle"}).getText().strip()

    # Fix the unprintable unicode characters
    df1 = df.applymap(lambda x: unidecode.unidecode(x))
    df = df1

    return df

def fund_asset_allocation(ticker):
    """
    Description:
    Get etf or fund asset allocation. Does not work for stocks.
    
    Parameters:
    ticker - The etf or fund ticker.

    Returs: 
    DataFrame with the performance history. 
    Run 'morningstar.py aas ticker' to see the result format.
    """
    # The Morningstar URL
    url = "http://portfolios.morningstar.com/fund/summary?t="
    
    # Get the table
    df = web.get_web_page_table(url + ticker, False, 1)

    # Create new dataframe from rows 0, 3, 5, 7, 9, 11
    df1 = pd.DataFrame(columns = range(7), 
                       index = range(6))

    df1.iloc[0] = df.iloc[0]
    df1.iloc[1] = df.iloc[3]
    df1.iloc[2] = df.iloc[5]
    df1.iloc[3] = df.iloc[7]
    df1.iloc[4] = df.iloc[9]
    df1.iloc[5] = df.iloc[11]

    # Special handling of two cells
    df1.iloc[0, 0] = df.iloc[1, 0]
    df1.iloc[0, 5] = "Benchmark" 

    df = df1

    # Fix the unprintable unicode characters
    df1 = df.applymap(lambda x: unidecode.unidecode(str(x)))
    df = df1

    # Promote 1st row and column as labels
    df1 = web.dataframe_promote_1st_row_and_column_as_labels(df)
    df = df1

    return df

def fund_market_capitalization(ticker):
    """
    Description:
    Get etf or fund market capitalization. Does not work for stocks.
    
    Parameters:
    ticker - The etf or fund ticker.

    Returs: 
    DataFrame with the performance history. 
    Run 'morningstar.py aas ticker' to see the result format.
    """
    # The Morningstar URL
    url = "http://portfolios.morningstar.com/fund/summary?t="
    
    # Get the table
    df = web.get_web_page_table(url + ticker, False, 2)

    # Create new dataframe from rows 0, 2, 4, 6, 8, 10
    df1 = pd.DataFrame(columns = range(4), 
                       index = range(6))

    df1.iloc[0] = df.iloc[0]
    df1.iloc[1] = df.iloc[2]
    df1.iloc[2] = df.iloc[4]
    df1.iloc[3] = df.iloc[6]
    df1.iloc[4] = df.iloc[8]
    df1.iloc[5] = df.iloc[10]

    df = df1

    # Promote 1st row and column as labels
    df1 = web.dataframe_promote_1st_row_and_column_as_labels(df)
    df = df1

    return df

def fund_sector_weightings(ticker):
    """
    Description:
    Get etf or fund sector weightings. Does not work for stocks.
    
    Parameters:
    ticker - The etf or fund ticker.

    Returs: 
    DataFrame with the performance history. 
    Run 'morningstar.py aas ticker' to see the result format.
    """
    # The Morningstar URL
    url = "http://portfolios.morningstar.com/fund/summary?t="
    
    # Get the table
    df = web.get_web_page_table(url + ticker, False, 5)

    df.fillna(value="", inplace=True)

    # Create new dataframe from rows 0, 2, 4, 6, 8, 10
    df1 = pd.DataFrame(columns = range(8), 
                       index = range(12))

    df1.iloc[0] = df.iloc[0]
    df1.iloc[1] = df.iloc[4]
    df1.iloc[2] = df.iloc[6]
    df1.iloc[3] = df.iloc[8]
    df1.iloc[4] = df.iloc[10]
    df1.iloc[5] = df.iloc[15]
    df1.iloc[6] = df.iloc[17]
    df1.iloc[7] = df.iloc[19]
    df1.iloc[8] = df.iloc[21]
    df1.iloc[9] = df.iloc[26]
    df1.iloc[10] = df.iloc[28]
    df1.iloc[11] = df.iloc[30]

    df1.iloc[0, 0] = "Type"
    df1.iloc[0, 1] = "Category"
    df1.iloc[1, 1] = "Cyclical"
    df1.iloc[2, 1] = "Cyclical"
    df1.iloc[3, 1] = "Cyclical"
    df1.iloc[4, 1] = "Cyclical"
    df1.iloc[5, 1] = "Sensitive"
    df1.iloc[6, 1] = "Sensitive"
    df1.iloc[7, 1] = "Sensitive"
    df1.iloc[8, 1] = "Sensitive"
    df1.iloc[9, 1] = "Defensive"
    df1.iloc[10, 1] = "Defensive"
    df1.iloc[11, 1] = "Defensive"

    # Remove column 5
    del df1[5]

    df = df1

    # Promote 1st row and column as labels
    df1 = web.dataframe_promote_1st_row_and_column_as_labels(df)
    df = df1

    return df

def fund_market_regions(ticker):
    """
    Description:
    Get etf or fund market regions. Does not work for stocks.
    
    Parameters:
    ticker - The etf or fund ticker.

    Returs: 
    DataFrame with the performance history. 
    Run 'morningstar.py aas ticker' to see the result format.
    """
    # The Morningstar URL
    url = "http://portfolios.morningstar.com/fund/summary?t="
    
    # Get the table
    df = web.get_web_page_table(url + ticker, False, 6)

    df.fillna(value="", inplace=True)

    # Create new dataframe from rows 0, 2, 4, 6, 8, 10
    df1 = pd.DataFrame(columns = range(4), 
                       index = range(10))

    df1.iloc[0] = df.iloc[0]
    df1.iloc[1] = df.iloc[5]
    df1.iloc[2] = df.iloc[7]
    df1.iloc[3] = df.iloc[11]
    df1.iloc[4] = df.iloc[13]
    df1.iloc[5] = df.iloc[15]
    df1.iloc[6] = df.iloc[21]
    df1.iloc[7] = df.iloc[23]
    df1.iloc[8] = df.iloc[25]
    df1.iloc[9] = df.iloc[27]

    df = df1

    # Fix the unprintable unicode characters
    df1 = df.applymap(lambda x: unidecode.unidecode(str(x)))
    df = df1

    # Promote 1st row and column as labels
    df1 = web.dataframe_promote_1st_row_and_column_as_labels(df)
    df = df1

    return df

def fund_market_classification(ticker):
    """
    Description:
    Get etf or fund market classification. Does not work for stocks.
    
    Parameters:
    ticker - The etf or fund ticker.

    Returs: 
    DataFrame with the performance history. 
    Run 'morningstar.py aas ticker' to see the result format.
    """
    # The Morningstar URL
    url = "http://portfolios.morningstar.com/fund/summary?t="
    
    # Get the table
    df = web.get_web_page_table(url + ticker, False, 5)

    df.fillna(value="", inplace=True)

    # Create new dataframe from rows 0, 2, 4, 6, 8, 10
    df1 = pd.DataFrame(columns = range(8), 
                       index = range(12))

    df1.iloc[0] = df.iloc[0]
    df1.iloc[1] = df.iloc[4]
    df1.iloc[2] = df.iloc[6]
    df1.iloc[3] = df.iloc[8]
    df1.iloc[4] = df.iloc[10]
    df1.iloc[5] = df.iloc[15]
    df1.iloc[6] = df.iloc[17]
    df1.iloc[7] = df.iloc[19]
    df1.iloc[8] = df.iloc[21]
    df1.iloc[9] = df.iloc[26]
    df1.iloc[10] = df.iloc[28]
    df1.iloc[11] = df.iloc[30]

    df1.iloc[0, 0] = "Type"
    df1.iloc[0, 1] = "Category"
    df1.iloc[1, 1] = "Cyclical"
    df1.iloc[2, 1] = "Cyclical"
    df1.iloc[3, 1] = "Cyclical"
    df1.iloc[4, 1] = "Cyclical"
    df1.iloc[5, 1] = "Sensitive"
    df1.iloc[6, 1] = "Sensitive"
    df1.iloc[7, 1] = "Sensitive"
    df1.iloc[8, 1] = "Sensitive"
    df1.iloc[9, 1] = "Defensive"
    df1.iloc[10, 1] = "Defensive"
    df1.iloc[11, 1] = "Defensive"

    # Remove column 5
    del df1[5]

    df = df1

    # Promote 1st row and column as labels
    df1 = web.dataframe_promote_1st_row_and_column_as_labels(df)
    df = df1

    return df

def _parse_pfh_f(args):
    df = fund_performance_history(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_pfh2_f(args):
    df = fund_performance_history2(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_ttl_f(args):
    df = trailing_total_returns(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_ttl2_f(args):
    df = fund_trailing_total_returns2(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_qtr_f(args):
    df = historical_quarterly_returns(args.ticker, args.years, args.frequency)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_qtr2_f(args):
    df = fund_historical_quarterly_returns(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_sp(args):
    df = stock_price(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_nav(args):
    df = net_asset_value(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_aal(args):
    df = fund_asset_allocation(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_mkc(args):
    df = fund_market_capitalization(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_sect(args):
    df = fund_sector_weightings(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_reg(args):
    df = fund_market_regions(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

def _parse_mks(args):
    df = fund_market_classification(args.ticker)
    print(tabulate(df, headers='keys', tablefmt='psql'))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download Morningstar data.')

    # Subparsers
    subparsers = parser.add_subparsers(help='Sub-command help')

    parser_pfh = subparsers.add_parser('pfh', help='Performace history')
    parser_pfh.add_argument('ticker', help='Ticker')
    parser_pfh.set_defaults(func=_parse_pfh_f)

    parser_pfh2 = subparsers.add_parser('pfh2', help='Performace history 2')
    parser_pfh2.add_argument('ticker', help='Ticker')
    parser_pfh2.set_defaults(func=_parse_pfh2_f)

    parser_ttl = subparsers.add_parser('ttl', help='Trailing total returns')
    parser_ttl.add_argument('ticker', help='Ticker')
    parser_ttl.set_defaults(func=_parse_ttl_f)

    parser_ttl2 = subparsers.add_parser('ttl2', help='Trailing total returns 2')
    parser_ttl2.add_argument('ticker', help='Ticker')
    parser_ttl2.set_defaults(func=_parse_ttl2_f)

    parser_qtr = subparsers.add_parser('qtr', help='Historical quarterly returns')
    parser_qtr.add_argument('ticker', help='Ticker')
    parser_qtr.add_argument('-y', '--years', type=int, default=5, help='Number of years (default 5)')
    parser_qtr.add_argument('-f', '--frequency', default='m', help='Frequency (m=monthly, q=quarterly, default=m)')
    parser_qtr.set_defaults(func=_parse_qtr_f)

    parser_qtr2 = subparsers.add_parser('qtr2', help='Historical quarterly returns for etfs and funds')
    parser_qtr2.add_argument('ticker', help='Ticker')
    parser_qtr2.set_defaults(func=_parse_qtr2_f)

    parser_sp = subparsers.add_parser('sp', help='Stock price')
    parser_sp.add_argument('ticker', help='Ticker')
    parser_sp.set_defaults(func=_parse_sp)

    parser_nav = subparsers.add_parser('nav', help='Mutual fund net asset value')
    parser_nav.add_argument('ticker', help='Ticker')
    parser_nav.set_defaults(func=_parse_nav)

    parser_aal = subparsers.add_parser('aal', help='Mutual fund asset allocation')
    parser_aal.add_argument('ticker', help='Ticker')
    parser_aal.set_defaults(func=_parse_aal)

    parser_mkc = subparsers.add_parser('mkc', help='Mutual fund market capitalization')
    parser_mkc.add_argument('ticker', help='Ticker')
    parser_mkc.set_defaults(func=_parse_mkc)

    parser_sect = subparsers.add_parser('sect', help='Mutual fund sector weightings')
    parser_sect.add_argument('ticker', help='Ticker')
    parser_sect.set_defaults(func=_parse_sect)

    parser_reg = subparsers.add_parser('reg', help='Mutual fund world regions')
    parser_reg.add_argument('ticker', help='Ticker')
    parser_reg.set_defaults(func=_parse_reg)

    parser_mks = subparsers.add_parser('mks', help='Mutual fund market classification')
    parser_mks.add_argument('ticker', help='Ticker')
    parser_mks.set_defaults(func=_parse_mks)

    args = parser.parse_args()
    args.func(args)
