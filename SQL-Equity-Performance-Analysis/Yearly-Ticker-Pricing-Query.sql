SELECT 
  	    Ticker,
  	    "Year",
  	    "Date",
  	    "Open",
  	    "High",
  	    "Low",
  	    "Close",
  	    "Volume"
FROM [Financial_Securities].[Equities].[VW_Yahoo_Equity_Year_Prices]
WHERE Ticker = 'MSFT'
ORDER BY "Year";