# SQL Equity Performance Analysis

## Create Equity Yearly Price View: *[Create-VW_Yahoo_Equity_Year_Prices-View.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Create-VW_Yahoo_Equity_Year_Prices-View.sql)*

Let's start by doing some analysis on yearly pricing data. We can aggregate the data in the *Yahoo_Equity_Prices* table and create a view called *VW_Yahoo_Equity_Year_Prices* that we will use in the project. Here we make use of various **WINDOW functions** to capture the **last date** of the year by Ticker using **MAX**. The *Date* for yearly data will be represented by the **last date**. We'll get the 1st Open price by Ticker and year as *"Open"* using **FIRST_VALUE**, the highest High price by Ticker and year as *"High"* using **MAX**, the lowest Low price by Ticker and year as *"Low"* using **MIN**, the last Close price by Ticker and year as *"Close"* using **LAST_VALUE**, and the last Volume by Ticker and year as *"Volume"* using **LAST_VALUE**. We group the data using **PARTITION BY** Ticker_ID and Year, **ORDER BY** date and use **UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING** clauses to scan and all the rows within the year. In doing so, duplication of our desired output will occur for all the records by year by ticker and to produce unique values, we can use **ROW_NUMBER**() as *Row_Num* and query for *Row_Num = 1*.

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
 		ROW_NUMBER()OVER (PARTITION BY q2.Ticker_ID, YEAR(q2.Date) ORDER BY q2.Date DESC) AS Row_Num
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


## Yearly Ticker Pricing Query Function: *[Create-FN_Yahoo_Ticker_Year_Prices.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Create-FN_Yahoo_Ticker_Year_Prices.sql)*

Let's create a function called *FN_Yahoo_Ticker_Year_Prices* that will query the yearly pricing view for a Ticker that is passed as a parameter.

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
 
  Let's query the yearly pricing data for the **MSFT** Ticker using our function *FN_Yahoo_Ticker_Year_Prices* and observe the results.

  	SELECT *
	FROM [Financial_Securities].[Equities].[FN_Yahoo_Ticker_Year_Prices]('MSFT')
	ORDER BY "Year";

 ![MSFT Yearly Pricing Data](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Yearly_Pricing_Data.jpg?raw=true)


## Yearly Ticker % Return Query Function: *[Create-FN_Yahoo_Ticker_Year_Returns.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Create-FN_Yahoo_Ticker_Year_Returns.sql)*

Let's create a function called *FN_Yahoo_Ticker_Year_Returns* that will query the yearly returns using the yearly pricing view for a Ticker that is passed as a parameter. Here we use the **LAG** WINDOW function to get prior year Close price and we don't have a prior Close price such as for 2021, we will use the Open price to calculate returns.

	CREATE OR ALTER FUNCTION [Equities].[FN_Yahoo_Ticker_Year_Returns](@input nchar(10))
	RETURNS TABLE
	AS
	RETURN
		SELECT
			Ticker,
			"Year",
			"Date",
			CASE
				WHEN COALESCE(LAG("Close", 1) OVER (PARTITION BY Ticker_ID ORDER BY "Date"), 0) = 0 THEN ROUND((("Close" / "Open") - 1.0) * 100, 2)
				ELSE ROUND((("Close" / LAG("Close", 1) OVER (PARTITION BY Ticker_ID ORDER BY "Date")) - 1.0) * 100, 2)
			END AS "% Return"
		FROM [Financial_Securities].[Equities].[VW_Yahoo_Equity_Year_Prices]
		WHERE Ticker = @input;

Let’s examine the Yearly returns for **Microsoft (MSFT)** to see which year had the lowest and highest returns.

  	SELECT *
	FROM [Financial_Securities].[Equities].[FN_Yahoo_Ticker_Year_Returns]('MSFT')
	ORDER BY "Year";

 ![MSFT_Yearly_Returns_Data.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Yearly_Returns_Data.jpg?raw=true)
 
We can observe that in the past 4 years, **MSFT** had the lowest return of **-28.02%** in **2022** and the highest return of **58.19%** in **2023**.

## Create Equity Yearly Price View: *[Create-VW_Yahoo_Equity_Quarter_Prices-View.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Create-VW_Yahoo_Equity_Quarter_Prices-View.sql)*

We create a Quarterly Returns function like the logic in the Yearly Returns function but based on Year and Quarter.

## Quarterly Ticker % Return Query Function: *[Create-FN_Yahoo_Ticker_Quarter_Returns.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Create-FN_Yahoo_Ticker_Quarter_Returns.sql)*

Let's now examine Quarter returns for **MSFT** to see if we can identify the reasons for worst year and best year returns.

	SELECT *
	FROM [Financial_Securities].[Equities].[FN_Yahoo_Ticker_Quarter_Returns]('MSFT')
	ORDER BY "Year", "Quarter";

 ![MSFT_Quarterly_Returns_Data.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Quarterly_Returns_Data.jpg?raw=true)

We can observe **MSFT** had **3 Quarters** in **2023** with high returns of roughly **18% to 20%** which impacted to the high return of **58.19%** in **2023**. And we had low returns in the **1st** and **3rd Quarter** of **2022** and a significant return of **-16.5%** in the **2nd Quarter** of **2022**. This impacted the low return of **-28.02%** in **2022**.


## Quarterly Ticker % Return by Year Statistics Query Function: *[Create-FN_Yahoo_Ticker_Quarter_Returns_by_Year_Statistics.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Create-FN_Yahoo_Ticker_Quarter_Returns_by_Year_Statistics.sql)*

Now let’s explore some statistical measures in SQL using Quarterly Returns. One statistical measure, called the **Median**, does not have a direct function in SQL Server. For more information on the Median, refer to this link: [Median: What It Is and How to Calculate It, With Examples](https://www.investopedia.com/terms/m/median.asp). Let's derive the Median Quarterly Return by year for the Ticker that is specified. We can use the concept of counting how many Quarters exist each year and if there are an even number of Quarters, we retrieve the 2 middle rows and if there is an odd number of Quarters, we retrieve the singular middle row. We then apply the average which works in both cases to the find the Median. We can also retrieve the lowest Quarterly Return, the highest Quarterly Return, average Quarterly Return, median Quarterly return and Quarterly return variance for a Ticker specified combining Yearly returns with Quarterly Returns, calculating the Median using the logic we explored and using the built-in SQL aggregate functions:  **MIN**, **MAX**, **AVG** and **STDEVP** (standard deviation). Here is the complex query that will produce the Quarterly Return Statistics by Year.

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

Let's find out what the lowest Quarterly Return, the highest Quarterly Return, average Quarterly Return, median Quarterly return and Quarterly return variance by year is for **MSFT**.

	SELECT *
	FROM [Financial_Securities].[Equities].[FN_Yahoo_Ticker_Quarter_Returns_by_Year_Statistics]('MSFT')
	ORDER BY "Year";

![MSFT_Quarterly_Return_by_Year_Statistics_Data.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Quarterly_Return_by_Year_Statistics_Data.jpg?raw=true)

Looking at **2022**, the average quarterly return was **-7.63%** which is higher than the median quarterly return of **-8.64%** and we can see that the positive **3.26%** highest return in Q4 had an impact. The highest variance appears to be in **2023** at **11.5%** and we can see a very high Median of **18.86%** is close the highest return of **20.51%** indicating that there were Quarters that had returns that were much lower. We can see that the lowest negative return of **-7.08%** in Q3 had a strong impact on variance from the average.

## Yearly Equity Return Ranking Query: *[Yearly-Equity-Return-Ranking-Query.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Yearly-Equity-Return-Ranking-Query.sql)*

If we want to compare which stocks from the S&P 500 performed the best by Year, we can use the **DENSE_RANK()** WINDOW function ranking yearly returns in descending order. Let's get the TOP 5 performing stocks by year with this query.

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

![SP500_Equity_Top_5_Returns_by_Year_Data.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Equity_Top_5_Returns_by_Year_Data.jpg?raw=true)

We see that **NVDA** is in the top 5 in all 5 years except 2022. **SMCI** and **CEG** are the only other stock that appears more than once. Both **NVDA** and **SMCI** are computer hardware types and in one of the top performing industries of the decade. 

## Yearly Equity Return Percentile Query: *[Yearly-Equity-Return-Percentile-Query.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Yearly-Equity-Return-Percentile-Query.sql)*

We can also look at bucketing yearly performance in percentiles using the **NTILE** WINDOW function. The top performing stocks would be in the highest percentile (100) and worst performing stocks would be in the lowest percentile (1). Let's query stocks from the S&P 500 that were in the 100th percentile.

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
		  NTILE(100) OVER(PARTITION BY q1."Year" ORDER BY q1."% Return" ASC) AS "% Return Percentile"
		FROM q1)
		SELECT
		  q2."Year",
		  q2.Ticker,
		  q2."% Return",
		  q2."% Return Rank"
		FROM q2
		WHERE q2."% Return Percentile" = 100
		ORDER BY q2."Year", q2."% Return" DESC;

![SP500_Equity_100th_Percentile_Returns_by_Year_Data.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Equity_100th_Percentile_Returns_by_Year_Data.jpg?raw=true)

Because we are bucketing in 100 different ranges depending how the returns are dispersed, you may get a different ranking range. For 2021 and 2022, we only got 4 stocks in the top 100th percentile. This time around, **NVDA** appeared 2 out of 4 years, **CEG** appeared 2 out of 4 years and **SMCI** appears once.

## Equity Cumulative Return Rank Query: *[Equity-Cumulative-Return-Rank-Query.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Equity-Cumulative-Return-Rank-Query.sql)*

Comparing simple returns by year by Ticker gives you a good idea of which stocks performed the best at the end of the year. And if we want to compare stocks across a longer timeframe, we could calculate the simple returns for all 4 years. But what if we did not have prices but only had returns? We could not add these simple returns to capture a total. We could use geometric mean but the simplest way is to use **Log Returns** since they are **additive**. This basically captures the compounding effect and gives a more accurate picture of long-term performance. Also, with simple returns, periods of high volatility with large positive or negative returns can skew the perception of a stock’s performance at a certain point in time. With log returns, we can capture volatility and risk much better. Let’s explore using daily log returns to capture the cumulative returns over the past 4 years. The cumulative returns are calculated by subtracting 1 from the exponential of the sum of all the log returns for a stock. Let’s do this in SQL using the LOG, SUM and EXP functions.

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

![SP500_Equity_Top_10_Cumulative_Returns_Data.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Equity_Top_10_Cumulative_Returns_Data.jpg?raw=true)

Here we see that **SMCI** had the highest cumulative return across the span of 4 years even though **NVDA** was in the top 5 performing stock using simple returns in most years. Of course, cumulative returns don't consider any drawdowns that could have occurred on a monthly, quarterly or yearly basis. Usually, the best performing stocks come with a risk to volatility and it's a price to pay for higher returns over time. What's interesting is the **LLY** appear in the top 10 cumulative returns but did not appear in the top 5 in any of the past 4 years. This indicates that **LLY** was trending with less volatility than the top performing stocks.





    
 
 

 

  

  
