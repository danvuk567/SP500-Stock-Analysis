CREATE OR ALTER FUNCTION [Equities].[FN_Yahoo_Ticker_Year_Prices](@input nchar(10))
RETURNS TABLE
AS
RETURN
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
	WHERE Ticker = @input;
