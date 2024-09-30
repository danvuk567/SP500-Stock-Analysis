CREATE OR ALTER FUNCTION [Equities].[FN_Yahoo_Ticker_Quarter_Returns](@input nchar(10))
RETURNS TABLE
AS
RETURN
	SELECT
		Ticker,
		"Year",
		"Quarter",
		"Date",
		CASE
			WHEN COALESCE(LAG("Close", 1) OVER (PARTITION BY Ticker_ID ORDER BY "Date"), 0) = 0 THEN ROUND((("Close" / "Open") - 1.0) * 100, 2)
			ELSE ROUND((("Close" / LAG("Close", 1) OVER (PARTITION BY Ticker_ID ORDER BY "Date")) - 1.0) * 100, 2)
		END AS "% Return"
	FROM [Financial_Securities].[Equities].[VW_Yahoo_Equity_Quarter_Prices]
	WHERE Ticker = @input;
