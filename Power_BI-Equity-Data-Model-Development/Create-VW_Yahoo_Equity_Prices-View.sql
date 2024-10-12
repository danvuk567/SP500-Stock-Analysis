CREATE VIEW [Equities].[VW_Yahoo_Equity_Prices] AS
SELECT 
        q1.Date,
	q6.Sector_ID,
        TRIM(q6.Name) AS Sector,
	q5.Industry_Group_ID,
        TRIM(q5.Name) AS Industry_Group,
	q4.Industry_ID,
        TRIM(q4.Name) AS Industry,
	q3.Sub_Industry_ID,
        TRIM(q3.Name) AS Sub_Industry,
	q2.Ticker_ID,
        TRIM(q2.Ticker) AS Ticker,
	TRIM(q2.Name) AS Name,
        ROUND(q1.[Open], 2) AS "Open",
        ROUND(q1.[High], 2) AS "High",
        ROUND(q1.[Low], 2) AS "Low",
        ROUND(q1.[Close], 2) AS "Close",
        q1.Volume AS "Volume"
FROM [Financial_Securities].[Equities].[Yahoo_Equity_Prices] q1
INNER JOIN [Financial_Securities].[Equities].[Equities] q2
ON q1.Ticker_ID = q2.Ticker_ID
INNER JOIN [Financial_Securities].[Equities].[Sub_Industries] q3
ON q2.Sub_Industry_ID = q3.Sub_Industry_ID
INNER JOIN [Financial_Securities].[Equities].[Industries] q4
ON q3.Industry_ID = q4.Industry_ID
INNER JOIN [Financial_Securities].[Equities].[Industry_Groups] q5
ON q4.Industry_Group_ID = q5.Industry_Group_ID
INNER JOIN [Financial_Securities].[Equities].[Sectors] q6
ON q5.Sector_ID = q6.Sector_ID;