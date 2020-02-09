Yahoo link require Yahoo account login.

https://finance.yahoo.com/quote/SPY

https://finance.yahoo.com/quote/SPY/performance

https://finance.yahoo.com/quote/SPY/holdings

https://finance.yahoo.com/quote/SPY/risk

https://finance.yahoo.com/quote/SPY/history?p=SPY

https://query1.finance.yahoo.com/v7/finance/download/SPY?period1=728265600&period2=1581120000&interval=1d&events=history&crumb=NSlargkY7fV

Or, use yfinance plugin:
https://aroussi.com/post/python-yahoo-finance


import yfinance as yf

msft = yf.Ticker("MSFT")
df = msft.history(period="max")
"""
returns:
              Open    High    Low    Close      Volume  Dividends  Splits
Date
1986-03-13    0.06    0.07    0.06    0.07  1031788800        0.0     0.0
1986-03-14    0.07    0.07    0.07    0.07   308160000        0.0     0.0
...
2019-04-15  120.94  121.58  120.57  121.05    15792600        0.0     0.0
2019-04-16  121.64  121.65  120.10  120.77    14059700        0.0     0.0
"""
df.to_csv("MSFT_DATETIME.csv")