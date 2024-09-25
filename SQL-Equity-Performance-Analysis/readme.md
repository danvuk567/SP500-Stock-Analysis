# SQL Equity Performance Analysis

## Equity Yearly Price View: VW_Yahoo_Equity_Year_Prices.sql

Let's start by doing some analysis on yearly pricing data. We can aggregate the data in the Yahoo_Equity_Prices and create a view called *VW_Yahoo_Equity_Year_Prices* that we will use in the project. Here we make use of various WINDOW functions to capture the last date of the year using MAX, the 1st Open price using FIRST_VALUE, the highest High price using MAX, the lowest LOW price using MIN, the last Close price using LAST_VALUE, and the last Volume using LAST_VALUE. We group the data using PARTITION BY Ticker_ID and Year, ORDER BY date and use UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING clauses to scan and all the rows within the year. In doing so, duplication of our desired output wiil occur for all the records by year by ticker and in order to produce unique values, we can use ROW_NUMBER() as Row_Num and query for Row_Num = 1.

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
		WHERE q1.Row_Num = 1;
