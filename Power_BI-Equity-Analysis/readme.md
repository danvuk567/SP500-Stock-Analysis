# Power BI Equity Analysis Report

Before bringing in any data source in to Power BI to build a report, let's consolidate the data we need into a database view called *VW_Yahoo_Equity_Prices* in order to avoid bringing in unnecessary data. This is good practice when possibly dealing with large data sets and allows us to practice some data transformations in Power BI **Power Query**. We'll define the view joining the GICS Industry Dimension table hierarchy tables to the Fact table *Yahoo_Equity_Prices*.

## *[Create-Data-Warehouse-Objects.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Power_BI-Equity-Analysis/Create-VW_Yahoo_Equity_Prices-View.sql)*  

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

![Power_BI_Import_Yahoo_Equty_Prices_View.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Import_Yahoo_Equty_Prices_View.jpg?raw=true)

We'll click on **Transform** to load **Power Query**. We'll rename our view *VW_Yahoo_Equity_Prices* to *Equity_Prices* as a simpler naming convention. Next, we will need to extract the Dimension tables from the view. 

We'll start with extracting the *Sectors* Dimension table query by duplicating the Equity_Prices table query. We select *Sector_ID* and *Sector* columns and use *Remove Other Columns*. And lastly we use *Remove Duplicates*.

![Power_BI_Power_Query_Sectors_Transformation.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Power_Query_Sectors_Transformation.jpg?raw=true)

We extract our *Industry_Group* Dimension Dimension table query by duplicating the Equity_Prices table query. We select *Sector_ID*, *Industry_Group*, and *Industry_Group_ID* columns and use *Remove Other Columns* and then *Remove Duplicates*.

![Power_BI_Power_Query_Industry_Groups_Transformation.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Power_Query_Industry_Groups_Transformation.jpg?raw=true)

Then we extract our *Industries* Dimension Dimension table query by duplicating the Equity_Prices table query. We select *Industry_Group_ID*, *Industry*, and *Industry_ID* columns and use *Remove Other Columns* and then *Remove Duplicates*.

![Power_BI_Power_Query_Industries_Transformation.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Power_Query_Industries_Transformation.jpg?raw=true)

We also extract our *Sub_Industries* Dimension Dimension table query by duplicating the Equity_Prices table query. We select *Industry_ID*, *Sub_Industry*, and *Sub_Industry_ID* columns and use *Remove Other Columns* and then *Remove Duplicates*.

![Power_BI_Power_Query_Sub_Industries_Transformation.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Power_Query_Sub_Industries_Transformation.jpg?raw=true)

We extract our *Equities* Dimension Dimension table query by duplicating the Equity_Prices table query. We select *Industry_Group_ID*, *Industry*, and *Industry_ID* columns and use *Remove Other Columns* and then *Remove Duplicates*.

![Power_BI_Power_Query_Equities_Transformation.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Power_Query_Equities_Transformation.jpg?raw=true)

And lastly, we'll remove the unnecessary columns from *Equity_Prices* to normalize our data model by selecting *Date*, *Ticker_ID*, *Open*, *High*, *Low*, *Close* and *Volume* columns and use *Remove Other Columns*

![Power_BI_Power_Query_Equity_Prices_Transformation.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Power_Query_Equity_Prices_Transformation.jpg?raw=true)

Let's now join all the tables using foreign keys to create our initial data model.

![Power_BI_Initial_Data_Model.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Initial_Data_Model.jpg?raw=true)


We want to view our pricing data by Year, Quarter or Month and the best way to do that is to use and create a **Calendar** Dimension table. To do so, we can use an expression language native to Power BI called **DAX**. DAX stands for Data Analysis Expressions and we can create the DAX **calculated table** Calendar using the min and max dates from the *Equity_Prices* table. We define the columns *Date*, *Year*, Quarter*, *Month Long* (long name), *Month Short* (short name), *Month No* and *Day* with the following DAX code:

	Calendar = 
  		VAR StartDate = MIN(Equity_Prices[Date])
  		VAR EndDate = MAX(Equity_Prices[Date])

		RETURN
    		ADDCOLUMNS(
        		CALENDAR(StartDate, EndDate),
        		"Year", YEAR([Date]),
        		"Quarter", YEAR([Date]) & "Q" & QUARTER([Date]),  // Combining Year and Quarter as a string value
       		 "Month Long", FORMAT([Date], "MMMM"),
       		 "Month Short", FORMAT([Date], "MMM"),
        		"Month No", (YEAR([Date]) * 100) + MONTH([Date]),  // Combining Year and Month as a numeric value
        		"Day", DAY([Date])
    		)





