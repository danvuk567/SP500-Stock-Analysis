# SQL Equity Performance Analysis

## Create Equity Yearly Price View: *[Create-VW_Yahoo_Equity_Year_Prices-View.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Create-VW_Yahoo_Equity_Year_Prices-View.sql)*

Let's start by doing some analysis on yearly pricing data. We can aggregate the data in the *Yahoo_Equity_Prices* table and create a view called *VW_Yahoo_Equity_Year_Prices* that we will use in the project. Here we make use of various WINDOW functions to capture the last date of the year by Ticker using MAX. The "Date" for yearly data will be represented by the last date. We'll get the 1st Open price by Ticker and year as "Open" using FIRST_VALUE, the highest High price by Ticker and year as "High" using MAX, the lowest Low price by Ticker and year as "Low" using MIN, the last Close price by Ticker and year as "Close" using LAST_VALUE, and the last Volume by Ticker and year as "Volume" using LAST_VALUE. We group the data using PARTITION BY Ticker_ID and Year, ORDER BY date and use UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING clauses to scan and all the rows within the year. In doing so, duplication of our desired output wiil occur for all the records by year by ticker and in order to produce unique values, we can use ROW_NUMBER() as Row_Num and query for Row_Num = 1.

		CREATE VIEW [Equities].[VW_Yahoo_Equity_Year_Prices] AS
		WITH q1 AS
		(SELECT 
  		     q2.Ticker_ID,
   		     TRIM(q3.Ticker) AS Ticker,
		     YEAR(q2.Date) AS "Year",
		     MAX(q2.Date) OVER (PARTITION BY q2.Ticker_ID, YEAR(q2.Date) ORDER BY q2.Date ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS Date,
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

  ## Yearly Pricing Query: *[Yearly-Ticker-Pricing-Query.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Yearly-Ticker-Pricing-Query.sql)*

  Lest's query the yearly pricing view for the **MSFT** Ticker and observe the results.

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

 ![MSFT Yearly Pricing Data](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Yearly_Pricing_Data.jpg?raw=true)


## Yearly % Returns Query: *[Yearly-Ticker-Returns-Query.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Yearly-Ticker-Returns-Query.sql)*

Let’s examine the Yearly returns for ** Micorsoft (MSFT)** to see which year had the lowest and highest returns. Here we use the LAG WINDOW function to get prior year Close price and we don't have a prior Close price such as for 2021, we will use the Open price to calculate returns. Let's query the Yearly Returns for **MSFT**.

	SELECT
        Ticker,
	    "Year",
	    "Date",
	     CASE
		WHEN COALESCE(LAG("Close", 1) OVER (PARTITION BY Ticker_ID ORDER BY "Date"), 0) = 0 THEN ROUND((("Close" / "Open") - 1.0) * 100, 2)
		ELSE ROUND((("Close" / LAG("Close", 1) OVER (PARTITION BY Ticker_ID ORDER BY "Date")) - 1.0) * 100, 2)
	     END AS "% Return"
	FROM [Financial_Securities].[Equities].[VW_Yahoo_Equity_Year_Prices]
	WHERE Ticker = 'MSFT'
    ORDER BY "Year";

 ![MSFT Yearly Pricing Data](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Yearly_Returns_Data.jpg?raw=true)
 
We can observe that in the past 4 years, **MSFT** had the lowest return of highest return of **58.19%** in **2023**.

## Create Equity Yearly Price View: *[Create-VW_Yahoo_Equity_Quarter_Prices-View.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Create-VW_Yahoo_Equity_Quarter_Prices-View.sql)*

We create a Quarterly pricing view similar to the logic in the Yearly pricing view but based on Year and Quarter.

## Quarterly % Returns Query: *[Quarterly-Ticker-Returns-Query.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Quarterly-Ticker-Returns-Query.sql)*

Let's now examine where the lowest Quarter returns and highest Quarter returns occured for **MSFT**.

	SELECT
    	    Ticker,
    	    "Year",
    	    "Quarter"
    	    "Date",
    	    CASE
     	       WHEN COALESCE(LAG("Close", 1) OVER (PARTITION BY Ticker_ID ORDER BY "Date"), 0) = 0 THEN ROUND((("Close" / "Open") - 1.0) * 100, 2)
     	       ELSE ROUND((("Close" / LAG("Close", 1) OVER (PARTITION BY Ticker_ID ORDER BY "Date")) - 1.0) * 100, 2)
   	    END AS "% Return"
	FROM [Financial_Securities].[Equities].[VW_Yahoo_Equity_Quarter_Prices]
	WHERE Ticker = 'MSFT'
	ORDER BY "Year", "Quarter";

 





    
 
 

 

  

  
