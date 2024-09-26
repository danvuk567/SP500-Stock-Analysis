		# SQL Equity Performance Analysis

## Create Equity Yearly Price View: *[Create-VW_Yahoo_Equity_Year_Prices-View.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Create-VW_Yahoo_Equity_Year_Prices-View.sql)*

Let's start by doing some analysis on yearly pricing data. We can aggregate the data in the *Yahoo_Equity_Prices* table and create a view called *VW_Yahoo_Equity_Year_Prices* that we will use in the project. Here we make use of various **WINDOW functions** to capture the **last date** of the year by Ticker using **MAX**. The **Date** for yearly data will be represented by the **last date**. We'll get the 1st Open price by Ticker and year as **"Open"** using **FIRST_VALUE**, the highest High price by Ticker and year as **"High"** using **MAX**, the lowest Low price by Ticker and year as **"Low"** using **MIN**, the last Close price by Ticker and year as **"Close"** using **LAST_VALUE**, and the last Volume by Ticker and year as **"Volume"** using **LAST_VALUE**. We group the data using **PARTITION BY** Ticker_ID and Year, **ORDER BY** date and use **UNBOUNDED PRECEDING and UNBOUNDED FOLLOWING** clauses to scan and all the rows within the year. In doing so, duplication of our desired output wiil occur for all the records by year by ticker and in order to produce unique values, we can use **ROW_NUMBER**() as **Row_Num** and query for **Row_Num = 1**.

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

Let’s examine the Yearly returns for **Microsoft (MSFT)** to see which year had the lowest and highest returns. Here we use the **LAG** WINDOW function to get prior year Close price and we don't have a prior Close price such as for 2021, we will use the Open price to calculate returns. Let's query the Yearly Returns for **MSFT**.

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
 
We can observe that in the past 4 years, **MSFT** had the lowest return of **-28.02%** in **2022** and the highest return of **58.19%** in **2023**.

## Create Equity Yearly Price View: *[Create-VW_Yahoo_Equity_Quarter_Prices-View.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Create-VW_Yahoo_Equity_Quarter_Prices-View.sql)*

We create a Quarterly pricing view similar to the logic in the Yearly pricing view but based on Year and Quarter.

## Quarterly % Returns Query: *[Quarterly-Ticker-Returns-Query.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Quarterly-Ticker-Returns-Query.sql)*

Let's now examine Quarter returns for **MSFT** to see if we can identify the reasons for worst year and best year returns.

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

 ![MSFT Quarterly Returns Data](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Quarterly_Returns_Data.jpg?raw=true)

 We can observe **MSFT** had **3 Quarters** in **2023** with high returns of roughly **18% to 20%** which impacted to the high return of **58.19%** in **2023**. And we had low returns in the **1st** and **3rd Quarter** of **2022** and a significant return of **-16.5%** in the **2nd Quarter** of **2022**. This impacted the low return of **-28.02%** in **2022**.

## Quarterly % Return by Year Statistics Query: *[Quarterly-Ticker-Return-by-Year-Statistics-Query.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Quarterly-Ticker-Return-by-Year-Statistics-Query.sql)*

Now let’s explore some statistical measures in SQL using Quarterly Returns. One statisitical measure, called the **Median**, does not have a direct function in SQL Server. For more information on the Meidan, refer to this link: [Median: What It Is and How to Calculate It, With Examples](https://www.investopedia.com/terms/m/median.asp). Let's derive the Median Quarterly Return by year for **MSFT**. We can use the concept of counting how many Quarters exist in a given year and if there are an even number of Quarters, we retrieve the 2 middle rows and if there is an odd number of Quarters, we retrieve the singular middle row. We then apply the average which works in both cases to the find the Median. Here is the complex query that demonstrates how this can be calculated.

	WITH q1 AS
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
	  q2 AS (
	    SELECT
	        q1.Ticker_ID,
		q1.Ticker,
	        q1."Year",
	        q1."Quarter",
	        q1."% Return",
	        ROW_NUMBER() OVER (PARTITION BY q1.Ticker_ID, q1."Year" ORDER BY q1."% Return") AS Row_Num,
	        COUNT(*) OVER (PARTITION BY q1.Ticker_ID, q1."Year") AS Cnt
	    FROM q1)
	 SELECT
	    q2.Ticker_ID,
	    q2.Ticker,
	    q2."Year",
	    ROUND(AVG
	      (CASE 
	         WHEN q2.Cnt % 2 = 1 THEN 
                   CASE 
		     WHEN q2.Row_Num = (q2.Cnt + 1) / 2 THEN q2."% Return"
		     ELSE NULL 
		   END
               ELSE 
		  CASE 
		    WHEN q2.Row_Num IN ((q2.Cnt / 2), (q2.Cnt / 2) + 1) THEN q2."% Return"
		    ELSE NULL 
		  END
                END
	       ) * 100, 2) AS "Median % Return"
	 FROM q2
         WHERE q2.Row_Num IN ((q2.Cnt + 1) / 2, (q2.Cnt / 2) + 1)
         AND q2.Ticker = 'MSFT'
         GROUP BY q2.Ticker_ID, q2.Ticker, q2."Year";

Let's find out what the lowest Quarterly Return, the highest Quarterly Return, average Quarterly Return, median Quarterly return and Quarterly return variance is for **MSFT** combining Yearly returns with Quarterly Returns, calculating the Median using the logic we explored and using the built-in SQL aggregate functions:  **MIN**, **MAX**, **AVG** and **STDEVP** (standard deviation). Here is the complex query that will produce the Quarterly Return Statistics by Year.

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
		q3 AS (
		    SELECT
		        q2.Ticker_ID,
			q2.Ticker,
		        q2."Year",
		        q2."Quarter",
		        q2."% Return",
		        ROW_NUMBER() OVER (PARTITION BY q2.Ticker_ID, q2."Year" ORDER BY q2."% Return") AS Row_Num,
		        COUNT(*) OVER (PARTITION BY q2.Ticker_ID, q2."Year") AS Cnt
		    FROM q2
		),
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
		AND q1.Ticker = 'MSFT'
		GROUP BY 
 		   q1.Ticker,
 		   q1."Year",
  		   q1."% Return",
  		   q4."Median % Return"
		ORDER BY q1."Year";

![MSFT Quarterly Return by Year Statistics Data](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Quarterly_Return_by_Year_Statistics_Data.jpg?raw=true)

Looking at **2022**, the average quarterly return was **-7.63%** which is higher than the median quarterly return of **-8.64%** and we can see that the positive **3.26%** highest return in Q4 had an impact. The highest variance appears to be in **2023** at **11.5%** and we can see a very high Median of **18.86%** is close the highest return of **20.51%** indicating that there were Quarters that had returns that were much much lower. We can see that the lowest negative return of **-7.08%** in Q3 had a strong impact on variance from the average.

## Yearly Equity Return Ranking Query: *[Yearly-Equity-Return-Ranking-Query.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/SQL-Equity-Performance-Analysis/Yearly-Equity-Return-Ranking-Query.sql)*

If we want to compare which stocks from the S&P 500 performed the best by Year, we can use the **RANK** WINDOW function ranking yearly returns in descending order. Let's get the TOP 5 performing stocks by year with this query.

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
		  RANK() OVER(PARTITION BY q1."Year" ORDER BY q1."% Return" DESC) AS "% Return Rank"
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

We see that **NVDA** is in the top 5 in all 5 years except 2022. **SMCI** is the only other stock that appears more than once. Both **NVDA** and **SMCI** are computer hardware types and in one of the top performing industries of the decade. 








    
 
 

 

  

  
