# SQL Equity Performance Analysis

## Equity Yearly Price View: VW_Yahoo_Equity_Year_Prices.sql

Let's start by doing some analysis on yearly data. We can create a view called *VW_Yahoo_Equity_Year_Prices* that we will use in the project. We will use various WINDOW functions to aggregate data and capture the last date of the year using MAX, the 1st Open price using FIRST_VALUE, the highest High price using MAX, the lowest LOW price using MIN, the last Close price using LAST_VALUE, and the last Volume using LAST_VALUE. We group the data with PARTITION BY Ticker_ID and Year, ORDER BY date and we use UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING clauses to scan and retieve all the rows within the year. Since we will retrieve the all the records by year for each ticker and we only want one row, we can use ROW_NUMBER() as Row_Num and finally query for Row_Num = 1 to retrieve one row by Ticker.

CREATE VIEW VW_Yahoo_Equity_Year_Prices AS
WITH q1 AS
(SELECT 
        q2.Ticker_ID,
        TRIM(q3.Ticker) AS Ticker,
		YEAR(q2.Date) AS "Year",
		LAST_VALUE(q2.Date) OVER (PARTITION BY q2.Ticker_ID, YEAR(q2.Date) ORDER BY q2.Date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS Date,
		FIRST_VALUE(q2.[Open]) OVER (PARTITION BY q2.Ticker_ID, YEAR(q2.Date) ORDER BY q2.Date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS "Open",
		MAX(q2.[High]) OVER (PARTITION BY q2.Ticker_ID, YEAR(q2.Date) ORDER BY q2.Date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS "High",
        MIN(q2.[Low]) OVER (PARTITION BY q2.Ticker_ID, YEAR(q2.Date) ORDER BY q2.Date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS "Low",
        LAST_VALUE(q2.[Close]) OVER (PARTITION BY q2.Ticker_ID, YEAR(q2.Date) ORDER BY q2.Date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS "Close",
		LAST_VALUE(q2.Volume) OVER (PARTITION BY q2.Ticker_ID, YEAR(q2.Date) ORDER BY q2.Date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS "Volume",
        ROW_NUMBER() OVER (PARTITION BY q2.Ticker_ID, YEAR(q2.Date) ORDER BY q2.Date DESC) AS Row_Num
    FROM [Financial_Securities].[Equities].[Yahoo_Equity_Prices] q2
	INNER JOIN [Financial_Securities].[Equities].[Equities] q3
    ON q2.Ticker_ID = q3.Ticker_ID)
SELECT
    q1.Ticker_ID,
    q1.Ticker,
	q1."Year",
	q1.Date,
	ROUND(q1."Open", 2) AS "Open",
	ROUND(q1."High", 2) AS "High",
	ROUND(q1."Low", 2) AS "Low",
    ROUND(q1."Close", 2) AS "Close",
	q1.Volume
FROM q1
WHERE q1.Row_Num = 1
