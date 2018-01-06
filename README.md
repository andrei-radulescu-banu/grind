# findribble
Financial data scraped from the web. 

Web sites that could possibly be used for scraping - along with their download times:

http://quicktake.morningstar.com/fundnet/printreport.aspx?symbol=fusex (3-10 secs)
http://portfolios.morningstar.com/fund/summary?t=fusex (3-10 secs)
http://performance.morningstar.com/Performance/fund/trailing-total-returns.action?t=FSCTX (.1-.4 secs)
http://performance.morningstar.com/RatingRisk/fund/mpt-statistics.action?&t=SPY (.1-.4 secs)
http://quotes.morningstar.com/stock/c-header?&t=SPY (.1-.4 secs)
http://quotes.morningstar.com/fund/c-header?&t=FMXKX (.1-.4 secs)
http://etfs.morningstar.com/etf-preminumChart?&t=ARCX:VWO (quick) - discount prices
http://etfs.morningstar.com/latest-component?&t=ARCX:VWO (quick) - latest distributions
http://etfs.morningstar.com/quote-banner?&t=ARCX:VWO (quick) - intraday indicative value
http://performance.morningstar.com/Performance/fund/performance-history-1.action?&t=FUSEX&ops=clear&s=0P00001MK8&ndec=2&ep=true&align=m&y=6&comparisonRemove=false&loccat=&taxadj=&benchmarkSecId=&benchmarktype= (quick) - yearly performance history
http://performance.morningstar.com/Performance/fund/standardized-returns.action?&t=XNAS:FUSEX&region=usa&culture=en-US&cur=USD&ops=clear&s=0P00001MK8&ndec=2&ep=true&align=m&freq=d&discl=false&comparisonRemove=false&loccat=&taxadj=&benchmarkSecId=&benchmarktype= (quick) - Standardized returns include dividends and cap gains but not taxes
http://performance.morningstar.com/Performance/fund/historical-returns.action?&t=XNAS:FUSEX&region=usa&culture=en-US&cur=USD&ops=clear&s=0P00001MK8&ndec=2&ep=true&align=m&y=5&freq=q&comparisonRemove=false&loccat=&taxadj=&benchmarkSecId=&benchmarktype= (quick) - historical returns, quarters
http://performance.morningstar.com/Performance/fund/historical-returns.action?&t=XNAS:FUSEX&region=usa&culture=en-US&cur=USD&ops=clear&s=0P00001MK8&ndec=2&ep=true&align=m&y=5&freq=m&comparisonRemove=false&loccat=&taxadj=&benchmarkSecId=&benchmarktype= (quick) - historical returns, months