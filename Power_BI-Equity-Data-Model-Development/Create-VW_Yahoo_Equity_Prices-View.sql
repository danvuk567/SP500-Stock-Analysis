WITH q2
AS
(SELECT 
    	q1.Date,
    	q1.Ticker_ID,
    	ROUND(q1.[Open], 2) AS "Open",
    	ROUND(q1.[High], 2) AS "High",
    	ROUND(q1.[Low], 2) AS "Low",
    	ROUND(q1.[Close], 2) AS "Close",
    	q1.Volume AS "Volume"
FROM [Financial_Securities].[Equities].[Yahoo_Equity_Prices] q1
WHERE EXISTS (SELECT 1 FROM [Financial_Securities].[Equities].[Yahoo_Equity_Prices] WHERE Ticker_ID = q1.Ticker_ID AND Date = (SELECT MIN(Date) FROM [Financial_Securities].[Equities].[Yahoo_Equity_Prices]))),
q8 AS
(SELECT 
    	q2.Date,
	q7.Sector_ID,
    	TRIM(q7.Name) AS Sector,
	q6.Industry_Group_ID,
    	TRIM(q6.Name) AS Industry_Group,
	q5.Industry_ID,
    	TRIM(q5.Name) AS Industry,
	q4.Sub_Industry_ID,
    	TRIM(q4.Name) AS Sub_Industry,
	q3.Ticker_ID,
    	TRIM(q3.Ticker) AS Ticker,
	TRIM(q3.Name) AS Name,
    	ROUND(q2.[Open], 2) AS "Open",
    	ROUND(q2.[High], 2) AS "High",
    	ROUND(q2.[Low], 2) AS "Low",
    	ROUND(q2.[Close], 2) AS "Close",
    	q2.Volume AS "Volume"
FROM q2
INNER JOIN [Financial_Securities].[Equities].[Equities] q3
ON q3.Ticker_ID = q2.Ticker_ID
INNER JOIN [Financial_Securities].[Equities].[Sub_Industries] q4
ON q4.Sub_Industry_ID = q3.Sub_Industry_ID
INNER JOIN [Financial_Securities].[Equities].[Industries] q5
ON q5.Industry_ID = q4.Industry_ID
INNER JOIN [Financial_Securities].[Equities].[Industry_Groups] q6
ON q6.Industry_Group_ID = q5.Industry_Group_ID
INNER JOIN [Financial_Securities].[Equities].[Sectors] q7
ON q7.Sector_ID = q6.Sector_ID)
SELECT distinct q8.Ticker_ID
FROM q8;
