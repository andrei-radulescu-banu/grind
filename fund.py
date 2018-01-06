import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate

def morningstar_fund_performance_history(ticker):
    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = morningstar_parse_url_table(url, 12, ticker)

    # Trim last three rows
    df.drop(df.tail(3).index,inplace=True)

    return df

def morningstar_fund_trailing_total_returns(ticker):
    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = morningstar_parse_url_table(url, 14, ticker)

    return df 

def morningstar_fund_historical_quarterly_returns(ticker):
    # The Morningstar URL for funds
    url = "http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol="
    
    df = morningstar_parse_url_table(url, 16, ticker)

    return df 

def morningstar_parse_url_table(url, table_idx, ticker):
    # Get the page
    r = requests.get(url + ticker)

    # Parse the contents
    soup = BeautifulSoup(r.content,'lxml')

    # List of all tables
    tables = soup.find_all('table')

    # Specific tables
    table = tables[table_idx]

    # Get the number of rows and columns
    row_count = len(table.find_all('tr'))
    column_count = 0

    for row in table.find_all('tr'):
        column_idx = len(row.find_all('td'))
        if column_count < column_idx:
            column_count = column_idx
    
    #print("row_count = %s, column_count = %s"%(row_count, column_count))

    df = pd.DataFrame(columns = range(column_count), 
                      index = range(row_count))
    
    row_idx = 0
    for row in table.find_all('tr'):
        column_idx = 0
        columns = row.find_all('td')
        for column in columns:
            column_text = column.get_text()
    
            #print("row_idx %d, cloumn_idx %d, text %s" % (row_idx, column_idx, column_text))
            df.iat[row_idx, column_idx] = column_text
            column_idx += 1
        row_idx += 1

    df.set_value(0, 0, "New index")

    # Promote 1st row as column labels
    new_header = df.iloc[0] #grab the first row for the header
    df = df[1:] #take the data less the header row
    df.columns = new_header #set the header row as the df header
    
    # Promote 1st column as new index
    df2 = df.set_index("New index")
    df = df2
    df.index.name = ticker.upper()

    return df

if __name__ == "__main__":
    # execute only if run as a script
    if (len(sys.argv) == 2):
        #df = morningstar_fund_trailing_total_returns(sys.argv[1])
        #print(tabulate(df, headers='keys', tablefmt='psql'))

        #df = morningstar_fund_performance_history(sys.argv[1])        
        #print(tabulate(df, headers='keys', tablefmt='psql'))

        df = morningstar_fund_historical_quarterly_returns(sys.argv[1])        
        print(tabulate(df, headers='keys', tablefmt='psql'))
    else:
        print("Usage: %s ticker_symbol" % sys.argv[0])
