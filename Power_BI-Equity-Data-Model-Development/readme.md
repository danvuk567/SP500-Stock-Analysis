# Power BI Equity Data Model Development

Before bringing in any data source in to Power BI to build a report, let's consolidate the data we need into a database view called *VW_Yahoo_Equity_Prices* to avoid bringing in unnecessary data. This is good practice when possibly dealing with large data sets and allows us to practice some data transformations in Power BI **Power Query**. We want to compare the stocks that have been active throughout the whole period in to avoid any performance bias. To do that, we'll define the view joining the GICS Industry Dimension hierarchy tables to the Fact table *Yahoo_Equity_Prices* and filter out stocks that don't share the same min date of existing pricing data.

## *[Create-VW_Yahoo_Equity_Prices-View.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Power_BI-Equity-Analysis/Create-VW_Yahoo_Equity_Prices-View.sql)*  

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

![Power_BI_Import_Yahoo_Equty_Prices_View.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Import_Yahoo_Equty_Prices_View.jpg?raw=true)

We'll click on **Transform** to load **Power Query**. We'll rename our view *VW_Yahoo_Equity_Prices* to *Equity_Prices* as a simpler naming convention. Next, we will need to extract the Dimension tables from the view. 

We'll start with extracting the *Sectors* Dimension table query by duplicating the Equity_Prices table query. We select *Sector_ID* and *Sector* columns and use *Remove Other Columns*. And lastly, we use *Remove Duplicates*.

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

Let's now create relationships between all the tables we defined.

We'll create a **one-to-many relationship** between *Sector_ID* in the *Sectors* table to *Sector_ID* in the *Industry_Groups* table, a one-to-many relationship between *Industry_Group_ID* in the *Industry_Groups* table to *Industry_Group_ID* in the *Industries* table, a one-to-many relationship between *Industry_ID* in the *Industries* table to *Industry_ID* in the *Sub_Industries* table, a one-to-many relationship between *Sub_Industry_ID* in the *Sub_Industries* table to *Sub_Industry_ID* in the *Equities* table, and a one-to-many relationship between *Ticker_ID* in the *Equities* table to *Ticker_ID* in the *Equity_Prices* table. We'll also create a one-to-many relationship between *Date* in the *Calendar* table to *Date* in the *Equity_Prices* table.

![Power_BI_Pricing_Data_Model_Relationships.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Pricing_Data_Model_Relationships.jpg?raw=true)

And our initial Data Model now looks like this:

![Power_BI_Initial_Data_Model.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Initial_Data_Model.jpg?raw=true)

This project will require some custom table and fields that will be calculated using **DAX**. DAX stands for Data Analysis Expressions and is an expression language native to Power BI. The following link contains instruction and DAX code that we will refer to step by step going forward.

## *[DAX-Code-Instructions.txt](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Power_BI-Equity-Analysis/DAX-Code-Instructions.txt)*    

We want to view our pricing data by Year, Quarter or Month and to do that we'll first need to create a **Calendar** Dimension table using **New table** in the **Model View** section. We'll use **DAX** to create the **calculated table** Calendar using the min and max dates from the *Equity_Prices* table. We define the columns *Date*, *Year*, *Quarter*, *Month Long* (long name), *Month Short* (short name), *Month No* and *Day* with the following DAX code:

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

Next, in the **Data Pane**, we will use **New Column** to create the *Year*, *Quarter* and *Month No* **calculated columns** in the **Equity_Prices table** which we will use to create our aggregated calculated tables for Year, Quarter and Month.

 	Year = YEAR(Equity_Prices[Date])
    Quarter = YEAR([Date]) & "Q" & QUARTER([Date])
	Month No = (YEAR([Date]) * 100) + MONTH([Date])

The first pricing table we will create is called *Equity_Prices_by_Year* using DAX. We will use **SUMMARIZE** to aggregate the pricing data from *Equity_Prices*, **ALL** to use unfiltered data and group all column data by *Ticker_ID* and *Year*. We define the *Date* column as max date by Ticker_ID and Year. The *Open* column is complex as we need to use **CALCULATE** and get the first non-blank Open price using **FIRSTNONBLANK** function. We use **FILTER** on the unfiltered table to filter by conditions involving Ticker_ID and Year and **EARLIER** function to access a value from an earlier row when dealing with multiple layers of filters or iterations. We also need a Date match as well to pull one valid record. We'll need to use another sub calculation using CALCULATE, **MIN** function and EARLIER to get the min date by Ticker_ID and Year. The *High* column is simply calculated using the **MAX** function and is spanning all dates by Ticker_ID and Year. The *Low* column is simply calculated using the **MIN** function and is spanning all dates by Ticker_ID and Year. The *Close* column is calculated using similar conditional logic as the Open column calculation but instead uses the **LASTNONBLANK** function to pull the last non-blank Close price. And lastly, the *Volume* column is calculated the same way as the Close column. Here is the complex DAX code to achieve the desired results.

	Equity_Prices_by_Year = 
	SUMMARIZE(
    	ALL(Equity_Prices),  // Removes all filters on the Equity_Prices table
    	Equity_Prices[Ticker_ID],  // Group by Ticker_ID
    	Equity_Prices[Year],    // Group by Year

    	"Date", MAX(Equity_Prices[Date]),  // Get Max Date by Ticker and year
    
    	// Get the first 'Open' value by Ticker for the year (by MIN date)
    	"Open", 
           CALCULATE(
            	FIRSTNONBLANK(Equity_Prices[Open], 1),
            	FILTER(
                	ALL(Equity_Prices),  
                	Equity_Prices[Ticker_ID] = EARLIER(Equity_Prices[Ticker_ID]) &&
                	Equity_Prices[Year] = EARLIER(Equity_Prices[Year]) &&
                	Equity_Prices[Date] = CALCULATE(
                    	    MIN(Equity_Prices[Date]),
                    	    FILTER(
                        	ALL(Equity_Prices), 
                        	Equity_Prices[Ticker_ID] = EARLIER(Equity_Prices[Ticker_ID]) &&
                        	Equity_Prices[Year] = EARLIER(Equity_Prices[Year])
                    	    )
                	)
            	 )
           ),
    
    	// Get the max 'High' value by Ticker for the year
    	"High", 
        	CALCULATE(
            	MAX(Equity_Prices[High]),
            	FILTER(
                	ALL(Equity_Prices),
                	Equity_Prices[Ticker_ID] = EARLIER(Equity_Prices[Ticker_ID]) &&
                	Equity_Prices[Year] = EARLIER(Equity_Prices[Year])
            	)
       	 ),
    
    	// Get the min 'Low' value by Ticker for the year
    	"Low", 
     	   	CALCULATE(
     	        MIN(Equity_Prices[Low]),
     	        FILTER(
     	           	ALL(Equity_Prices),
     	           	Equity_Prices[Ticker_ID] = EARLIER(Equity_Prices[Ticker_ID]) &&
     	           	Equity_Prices[Year] = EARLIER(Equity_Prices[Year])
     	       )
      	  ),
    
    	// Get the last 'Close' value by Ticker for the year (by MAX date)
 	"Close", 
  	   CALCULATE(
   	        LASTNONBLANK(Equity_Prices[Close], 1),
    	        FILTER(
     	            ALL(Equity_Prices),  
     	            Equity_Prices[Ticker_ID] = EARLIER(Equity_Prices[Ticker_ID]) &&
      	            Equity_Prices[Year] = EARLIER(Equity_Prices[Year]) &&
     	            Equity_Prices[Date] = CALCULATE(
     	                MAX(Equity_Prices[Date]),
      	                FILTER(
                   	    ALL(Equity_Prices), 
                   	    Equity_Prices[Ticker_ID] = EARLIER(Equity_Prices[Ticker_ID]) &&
                            Equity_Prices[Year] = EARLIER(Equity_Prices[Year])
                        )
                    )
 	       )
      	  ),
    
    	// Get the last 'Volume' value fby Ticker for the year (by MAX date)
        "Volume", 
           CALCULATE(
                LASTNONBLANK(Equity_Prices[Volume], 1),
                FILTER(
                    ALL(Equity_Prices),  
                    Equity_Prices[Ticker_ID] = EARLIER(Equity_Prices[Ticker_ID]) &&
                    Equity_Prices[Year] = EARLIER(Equity_Prices[Year]) &&
                    Equity_Prices[Date] = CALCULATE(
                        MAX(Equity_Prices[Date]),
                        FILTER(
                            ALL(Equity_Prices), 
                            Equity_Prices[Ticker_ID] = EARLIER(Equity_Prices[Ticker_ID]) &&
                            Equity_Prices[Year] = EARLIER(Equity_Prices[Year])
                        )
                    )
              )
          )
    )

We will then use DAX to create another table called *Equity_Prices_by_Quarter* which aggregates pricing data by quarter, and a table called *Equity_Prices_by_Month* which aggregates pricing data by month in a similar fashion.
 
a good idea is also to display the last date pricing data in a card visual. To achieve this, we'll need to create some **DAX measures**. For the *Equity_Prices_by_Year* table, we'll go to the Data Panel, click on **New measure** and create the following measures: *YearLastDate* which represents the last Date, *YearLastOpen* which represents last Open, *YearLastHigh* which represents last High, *YearLastLow* which represents last Low, *YearLastClose* which represents last Close and *YearLastVolume* which represents last Volume by Year. Here is the simple DAX code to create these measures.   

	YearLastDate = 
	CALCULATE(
    	MAX(Equity_Prices_by_Year[Date]),
    	FILTER(
     	   Equity_Prices_by_Year,
     	   Equity_Prices_by_Year[Ticker_ID] = SELECTEDVALUE(Equity_Prices_by_Year[Ticker_ID])
    	)
	)

	YearLastOpen = 
	CALCULATE(
	    LASTNONBLANK(Equity_Prices_by_Year[Open], 1),
 	   FILTER(
 	       Equity_Prices_by_Year,
  	      Equity_Prices_by_Year[Ticker_ID] = SELECTEDVALUE(Equity_Prices_by_Year[Ticker_ID]) &&
  	      Equity_Prices_by_Year[Date] = MAX(Equity_Prices_by_Year[Date])
 	   )
	)

	YearLastHigh = 
	CALCULATE(
	    LASTNONBLANK(Equity_Prices_by_Year[High], 1),
	    FILTER(
	        Equity_Prices_by_Year,
	        Equity_Prices_by_Year[Ticker_ID] = SELECTEDVALUE(Equity_Prices_by_Year[Ticker_ID]) &&
	        Equity_Prices_by_Year[Date] = MAX(Equity_Prices_by_Year[Date])
	    )
	)

	YearLastLow = 
	CALCULATE(
	    LASTNONBLANK(Equity_Prices_by_Year[Low], 1),
	    FILTER(
	        Equity_Prices_by_Year,
	        Equity_Prices_by_Year[Ticker_ID] = SELECTEDVALUE(Equity_Prices_by_Year[Ticker_ID]) &&
	        Equity_Prices_by_Year[Date] = MAX(Equity_Prices_by_Year[Date])
	    )
	)

	YearLastClose = 
	CALCULATE(
	    LASTNONBLANK(Equity_Prices_by_Year[Close], 1),
	    FILTER(
	        Equity_Prices_by_Year,
	        Equity_Prices_by_Year[Ticker_ID] = SELECTEDVALUE(Equity_Prices_by_Year[Ticker_ID]) &&
	        Equity_Prices_by_Year[Date] = MAX(Equity_Prices_by_Year[Date])
	    )
	)

	YearLastVolume = 
	CALCULATE(
	    LASTNONBLANK(Equity_Prices_by_Year[Volume], 1),
	    FILTER(
	        Equity_Prices_by_Year,
 	       Equity_Prices_by_Year[Ticker_ID] = SELECTEDVALUE(Equity_Prices_by_Year[Ticker_ID]) &&
 	       Equity_Prices_by_Year[Date] = MAX(Equity_Prices_by_Year[Date])
	    )
	)

We'll do the same type of DAX code to create the last quarterly date pricing data in the Equity_Prices_by_Quarter table, last monthly date pricing data in the Equity_Prices_by_Month table and the last daily pricing data in the Equity_Prices table.

Next, we create new relationships to the calculated tables that we created. We'll create a **one-to-many relationship** between *Ticker_ID* in the *Equities* table to *Ticker_ID* in the *Equity_Prices_by_Year*, *Equity_Prices_by_Quarter* and *Equity_Prices_by_Month* tables. We'll also create a one-to-many relationship between *Date* in the *Calendar* table to *Date* in the *Equity_Prices_by_Year*, *Equity_Prices_by_Quarter* and *Equity_Prices_by_Month* tables.

![Power_BI_Pricing_Data_Model_Relationships2.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Pricing_Data_Model_Relationships2.jpg?raw=true)

And our Data Model now looks like this:

![Power_BI_Pricing_Data_Model.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Pricing_Data_Model.jpg?raw=true)

The main goal of this project was to look at measuring performance focused on Equity returns. As we did with pricing, we can focus on YEarly, Quarterly, Monthly and Daily Returns. We had previously explored this in the project using Python code so rather than going down a long and complex path with DAX, we can use **Python** in **Power Query** to create some tables. 

We'll start with the Yearly Returns and create a table called *Equity_Returns_by_Year* by duplicating the *Equity_Prices* table in Power Query and keeping only the *Date*, *Ticker_ID* and *Close* columns. Next we can click on the *Transform* menu and then *Run Python script* to transform the data into Yearly Returns. When working with pandas, the default pandas dataframe is called *dataset*. We will calculate the *% Return* and the *Cumulative % Return* using log returns by Ticker_ID and Year similar to what we did independently earlier on the project.


	import pandas as pd
	import numpy as np

	# Converting the 'Date' column in 'dataset' to datetime format; invalid parsing will be set to NaT
	dataset['Date'] = pd.to_datetime(dataset['Date'], errors='coerce')

	# Extracting the year from the 'Date' column and creating a new 'Year' column
	dataset['Year'] = dataset['Date'].dt.year

	# Grouping the dataset by 'Ticker_ID' and 'Year', aggregating various metrics for each group
	dataset2 = dataset.groupby(['Ticker_ID', 'Year']).agg(
 	           {
 	               'Date': 'last',   # Get the last date for each ticker and year
	                'Open': "first",  # Get the first opening price for each ticker and year
 	               'High': 'max',    # Get the maximum high price for each ticker and year
 	               'Low': 'min',     # Get the minimum low price for each ticker and year
  	              'Close': 'last',  # Get the last closing price for each ticker and year
  	              'Volume': 'last'  # Get the last volume for each ticker and year
   	         }
  	      ).reset_index()  # Resetting the index to keep 'Ticker_ID' and 'Year' as columns

	# Sorting the aggregated dataset by 'Ticker_ID' and 'Date'
	dataset2.sort_values(by=['Ticker_ID', 'Date'], inplace=True)

	# Creating a new column 'Prev Close' to hold the previous closing price for each ticker
	dataset2['Prev Close'] = dataset2.groupby('Ticker_ID')['Close'].shift(1)

	# Identifying the first period for each ticker where 'Prev Close' is NaN
	is_first_period = dataset2['Prev Close'].isna()

	# Initializing '% Return' column with zeros
	dataset2['% Return'] = 0

	# Calculating % Return for the first period using Open and Close prices
	dataset2.loc[is_first_period, '% Return'] = np.round((dataset2['Close'] / dataset2['Open']) - 1.0, 4)

	# Creating a boolean mask to identify rows with the same Ticker_ID as the previous row
	same_ticker = dataset2['Ticker_ID'] == dataset2['Ticker_ID'].shift(1)

	# Calculating % Return for subsequent periods for the same ticker
	dataset2.loc[~is_first_period & same_ticker, '% Return'] = np.round((dataset2['Close'] / dataset2['Prev Close']) - 1.0, 4)

	# Calculating Log Return for the first period
	dataset2.loc[is_first_period, 'Log Return'] = np.log(dataset2['Close'] / dataset2['Open']) 

	# Calculating Log Return for subsequent periods for the same ticker
	dataset2.loc[~is_first_period & same_ticker, 'Log Return'] = np.log(dataset2['Close'] / dataset2['Prev Close'])

	# Calculating Cumulative Log Return for each ticker by summing Log Returns
	dataset2['Cumulative Log Return'] = dataset2.groupby('Ticker_ID')['Log Return'].cumsum()

	# Calculating Cumulative % Return based on Cumulative Log Return
	dataset2['Cumulative % Return'] = np.round(np.exp(dataset2['Cumulative Log Return']) - 1.0, 4)

	# Updating 'dataset' with the transformed data in 'dataset2'
	dataset = dataset2

	# Deleting 'dataset2' to free up memory
	del dataset2

The dataframe *dataset* is returned as a table and after a few more cleanup steps in Power Query, we have the final table called *Equity_Returns_by_Year*.


