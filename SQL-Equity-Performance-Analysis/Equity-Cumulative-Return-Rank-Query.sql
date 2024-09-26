WITH q1 AS
(SELECT
   q2.Ticker_ID,
   TRIM(q3.Ticker) AS Ticker,
   YEAR(q2.Date) AS "Year",
   q2."Date",
   CASE
     WHEN COALESCE(LAG(q2."Close", 1) OVER (PARTITION BY q2.Ticker_ID ORDER BY q2."Date"), 0) = 0 THEN LOG(q2."Close" / q2."Open")
     ELSE LOG(q2."Close" / LAG(q2."Close", 1) OVER (PARTITION BY q2.Ticker_ID ORDER BY q2."Date"))
   END AS "Log % Return"
FROM [Financial_Securities].[Equities].[Yahoo_Equity_Prices] q2
INNER JOIN [Financial_Securities].[Equities].[Equities] q3
ON q2.Ticker_ID = q3.Ticker_ID),
q4 AS
(SELECT 
   q1.Ticker_ID,
   q1.Ticker,
   ROUND((EXP(SUM(q1."Log % Return")) - 1.0) * 100, 2) AS "Cumulative % Return"
FROM q1
GROUP BY 
  q1.Ticker_ID,
  q1.Ticker),
q5 AS
(
SELECT 
  q4.Ticker_ID,
  q4.Ticker,
  q4."Cumulative % Return",
  DENSE_RANK() OVER(ORDER BY q4."Cumulative % Return" DESC) AS "Cumulative % Return Rank"
FROM q4)
SELECT
  q5.Ticker,
  q5."Cumulative % Return",
  q5."Cumulative % Return Rank"
FROM q5
WHERE q5."Cumulative % Return Rank" <= 10
ORDER BY q5."Cumulative % Return Rank";