WITH q1 AS
    (SELECT
	Ticker_ID,
	Ticker,
	"Year",
	"Date",
	CASE
	   WHEN COALESCE(LAG("Close", 1) OVER (PARTITION BY Ticker_ID ORDER BY "Date"), 0) = 0 THEN ROUND((("Close" / "Open") - 1.0) * 100, 2)
	   ELSE ROUND((("Close" / LAG("Close", 1) OVER (PARTITION BY Ticker_ID ORDER BY "Date")) - 1.0) * 100, 2)
	END AS "% Return"
      FROM [Financial_Securities].[Equities].[VW_Yahoo_Equity_Year_Prices]),
q2 AS
    (SELECT 
       q1.Ticker_ID,
       q1.Ticker,
       q1."Year",
       q1."% Return",
       DENSE_RANK() OVER(PARTITION BY q1."Year" ORDER BY q1."% Return" DESC) AS "% Return Rank"
     FROM q1)
SELECT
  q2."Year",
  q2.Ticker,
  q2."% Return",
  q2."% Return Rank"
FROM q2
WHERE q2."% Return Rank" <= 5
ORDER BY q2."Year", q2."% Return Rank";
