CREATE OR ALTER FUNCTION [Equities].[FN_Yahoo_Ticker_Quarter_Returns_by_Year_Statistics](@input nchar(10))
RETURNS TABLE
AS
RETURN
	WITH q1 AS
	(SELECT
		Ticker_ID,
		Ticker,
		"Year",
		"Date",
		CASE
			WHEN COALESCE(LAG("Close", 1) OVER (PARTITION BY Ticker_ID ORDER BY "Date"), 0) = 0 THEN ("Close" / "Open") - 1.0
			ELSE ("Close" / LAG("Close", 1) OVER (PARTITION BY Ticker_ID ORDER BY "Date")) - 1.0
		END AS "% Return"
	FROM [Financial_Securities].[Equities].[VW_Yahoo_Equity_Year_Prices]),
	q2 AS
	(SELECT
		Ticker_ID,
		Ticker,
		"Year",
		"Quarter",
		"Date",
		 CASE
			WHEN COALESCE(LAG("Close", 1) OVER (PARTITION BY Ticker_ID ORDER BY "Date"), 0) = 0 THEN ("Close" / "Open") - 1.0
			ELSE ("Close" / LAG("Close", 1) OVER (PARTITION BY Ticker_ID ORDER BY "Date")) - 1.0
		 END AS "% Return"
	FROM [Financial_Securities].[Equities].[VW_Yahoo_Equity_Quarter_Prices]),
	q3 AS 
	(SELECT
		q2.Ticker_ID,
		q2.Ticker,
		q2."Year",
		q2."Quarter",
		q2."% Return",
		ROW_NUMBER() OVER (PARTITION BY q2.Ticker_ID, q2."Year" ORDER BY q2."% Return") AS Row_Num,
		COUNT(*) OVER (PARTITION BY q2.Ticker_ID, q2."Year") AS Cnt
	FROM q2),
	q4 AS (
	SELECT
		q3.Ticker_ID,
		q3.Ticker,
		q3."Year",
		AVG(CASE 
			WHEN q3.Cnt % 2 = 1 THEN 
				CASE 
					WHEN q3.Row_Num = (q3.Cnt + 1) / 2 THEN q3."% Return"
					ELSE NULL 
				END
			ELSE 
				CASE 
					WHEN q3.Row_Num IN ((q3.Cnt / 2), (q3.Cnt / 2) + 1) THEN q3."% Return"
					ELSE NULL 
				END
		    END) AS "Median % Return"
	FROM q3
	WHERE q3.Row_Num IN ((q3.Cnt + 1) / 2, (q3.Cnt / 2) + 1)
	GROUP BY q3.Ticker_ID, q3.Ticker, q3."Year")
	SELECT
		q1.Ticker,
		q1."Year",
		ROUND(q1."% Return" * 100, 2) AS "Yearly % Return",
		ROUND(MIN(q2."% Return") * 100, 2) AS "Lowest Quarterly % Return",
		ROUND(MAX(q2."% Return") * 100, 2) AS "Highest Quarterly % Return",
		ROUND(AVG(q2."% Return") * 100, 2) AS "Avg Quarterly % Return",
		ROUND(q4."Median % Return" * 100, 2) AS "Median Quarterly % Return",
		ROUND(STDEVP(q2."% Return") * 100, 2) AS "Quarterly % Variance"
	FROM q1
	INNER JOIN q2
	ON q1.Ticker_ID = q2.Ticker_ID
	AND q1."Year" = q2."Year"
	INNER JOIN q4
	ON q1.Ticker_ID = q4.Ticker_ID
	AND q1."Year" = q4."Year"
	AND q1.Ticker = @input
	GROUP BY 
		q1.Ticker,
		q1."Year",
		q1."% Return",
		q4."Median % Return"
