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

We'll click on **Transform** to load **Power Query**. We'll rename our view *VW_Yahoo_Equity_Prices* to *Equity_Prices* as a simpler naming convention for our Fact table. Next, we will need to extract the Dimension tables from the view. 

We'll start with extracting the *Sectors* Dimension table query by duplicating the Equity_Prices table query. We select *Sector_ID* and *Sector* columns and use *Remove Other Columns*. And lastly, we use *Remove Duplicates*.

![Power_BI_Power_Query_Sectors_Transformation.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Power_Query_Sectors_Transformation.jpg?raw=true)

We extract our *Industry_Group* Dimension Dimension table query by duplicating the Equity_Prices table query. We select *Sector_ID*, *Industry_Group*, and *Industry_Group_ID* columns and use *Remove Other Columns* and then *Remove Duplicates*.

![Power_BI_Power_Query_Industry_Groups_Transformation.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Power_Query_Industry_Groups_Transformation.jpg?raw=true)

Then we extract our *Industries* Dimension Dimension table query by duplicating the Equity_Prices table query. We select *Industry_Group_ID*, *Industry*, and *Industry_ID* columns and use *Remove Other Columns* and then *Remove Duplicates*.

![Power_BI_Power_Query_Industries_Transformation.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Power_Query_Industries_Transformation.jpg?raw=true)

We also extract our *Sub_Industries* Dimension Dimension table query by duplicating the Equity_Prices table query. We select *Industry_ID*, *Sub_Industry*, and *Sub_Industry_ID* columns and use *Remove Other Columns* and then *Remove Duplicates*.

![Power_BI_Power_Query_Sub_Industries_Transformation.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Power_Query_Sub_Industries_Transformation.jpg?raw=true)

We extract our *Equities* Dimension table query by duplicating the Equity_Prices table query. We select *Industry_Group_ID*, *Industry*, and *Industry_ID* columns and use *Remove Other Columns* and then *Remove Duplicates*.

![Power_BI_Power_Query_Equities_Transformation.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Power_Query_Equities_Transformation.jpg?raw=true)

And lastly, we'll remove the unnecessary columns from *Equity_Prices* to normalize our data model by selecting *Date*, *Ticker_ID*, *Open*, *High*, *Low*, *Close* and *Volume* columns and use *Remove Other Columns*

![Power_BI_Power_Query_Equity_Prices_Transformation.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Power_Query_Equity_Prices_Transformation.jpg?raw=true)

Let's now create relationships between all the tables we defined.

We'll create a **one-to-many relationship** between *Sector_ID* in the *Sectors* table to *Sector_ID* in the *Industry_Groups* table, a one-to-many relationship between *Industry_Group_ID* in the *Industry_Groups* table to *Industry_Group_ID* in the *Industries* table, a one-to-many relationship between *Industry_ID* in the *Industries* table to *Industry_ID* in the *Sub_Industries* table, a one-to-many relationship between *Sub_Industry_ID* in the *Sub_Industries* table to *Sub_Industry_ID* in the *Equities* table, and a one-to-many relationship between *Ticker_ID* in the *Equities* table to *Ticker_ID* in the *Equity_Prices* table. We'll also create a one-to-many relationship between *Date* in the *Calendar* table to *Date* in the *Equity_Prices* table.

![Power_BI_Pricing_Data_Model_Relationships.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Pricing_Data_Model_Relationships.jpg?raw=true)

And our initial Data Model now looks like this:

![Power_BI_Initial_Data_Model.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Initial_Data_Model.jpg?raw=true)

This project will require some custom table and fields that will be calculated using **DAX**. DAX stands for Data Analysis Expressions and is an expression language native to Power BI. The following link contains instruction and DAX code that we will refer to step by step going forward.

## *Python Code to further Transform Data*

To transform existing data into other tables using more complex logic, we can run Python scripts within the Transform section in Power Query. 

To create the *Equity_Returns_by_Year* table, which calculates Equity returns by year, we can run the following Python script. Both the simple *Yearly % Returns* as well as the *Cumulative Yearly % Returns* (using Log Returns) are caluclated by Ticker.

[Equity_Returns_by_Year_Python_Code.txt](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Power_BI-Equity-Data-Model-Development/Equity_Returns_by_Year_Python_Code.txt)

		# 'dataset' holds the input data for this script
		import pandas as pd
		import numpy as np

		dataset['Date'] = pd.to_datetime(dataset['Date'], errors='coerce')
		dataset['Year'] = dataset['Date'].dt.year

		dataset2 = dataset.groupby(['Ticker_ID', 'Year']).agg(
            		{
                		'Date': 'last',   # Get the last date for each group
                		'Open': "first",  # Get the first opening price for each group
                		'High': 'max',    # Get the maximum high price for each group
                		'Low': 'min',     # Get the minimum low price for each group
                		'Close': 'last',  # Get the last closing price for each group
                		'Volume': 'last'  # Get the last volume for each group
            		}
       		 ).reset_index() 

		dataset2.sort_values(by=['Ticker_ID', 'Date'], inplace=True)
		dataset2['Prev Close'] = dataset2.groupby('Ticker_ID')['Close'].shift(1)
		is_first_period = dataset2['Prev Close'].isna()

		dataset2['% Return'] = 0
		dataset2.loc[is_first_period, '% Return'] = np.round((dataset2['Close'] / dataset2['Open']) - 1.0, 4)
    
		same_ticker = dataset2['Ticker_ID'] == dataset2['Ticker_ID'].shift(1)
		dataset2.loc[~is_first_period & same_ticker, '% Return'] = np.round((dataset2['Close'] / dataset2['Prev Close']) - 1.0, 4)

		dataset2.loc[is_first_period, 'Log Return'] = np.log(dataset2['Close'] / dataset2['Open']) 
		dataset2.loc[~is_first_period & same_ticker, 'Log Return'] = np.log(dataset2['Close'] / dataset2['Prev Close'])

		dataset2['Cumulative Log Return'] = dataset2.groupby('Ticker_ID')['Log Return'].cumsum()
		dataset2['Cumulative % Return'] = np.round(np.exp(dataset2['Cumulative Log Return']) - 1.0, 4)

		dataset = dataset2

		del dataset2

To other Fact tables that will be transformed with Python are listed below along with their Python script.

*Equity_Returns_by_Quarter:*

[Equity_Returns_by_Quarter_Python_Code.txt](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Power_BI-Equity-Data-Model-Development/Equity_Returns_by_Quarter_Python_Code.txt)

*Equity_Returns_by_Month:*

[Equity_Returns_by_Month_Python_Code.txt](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Power_BI-Equity-Data-Model-Development/Equity_Returns_by_Month_Python_Code.txt)

*Equity_Returns:*

[Equity_Returns_Python_Code.txt](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Power_BI-Equity-Data-Model-Development/Equity_Returns_Python_Code.txt)

*Equity_Statistics:*

[Equity_Statistics_Python_Code.txt](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Power_BI-Equity-Data-Model-Development/Equity_Statistics_Python_Code.txt)


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

We'll do the same type of DAX code to create the last quarterly date pricing data in the *Equity_Prices_by_Quarter* table, last monthly date pricing data in the *Equity_Prices_by_Month* table and the last daily pricing data in the *Equity_Prices* table.

Next, we create new relationships to the calculated tables that we created. We'll create a **one-to-many relationship** between *Ticker_ID* in the *Equities* table to *Ticker_ID* in the *Equity_Prices_by_Year*, *Equity_Prices_by_Quarter* and *Equity_Prices_by_Month* tables. We'll also create a one-to-many relationship between *Date* in the *Calendar* table to *Date* in the *Equity_Prices_by_Year*, *Equity_Prices_by_Quarter* and *Equity_Prices_by_Month* tables.

![Power_BI_Pricing_Data_Model_Relationships2.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Pricing_Data_Model_Relationships2.jpg?raw=true)

And our Data Model now looks like this:

![Power_BI_Pricing_Data_Model.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Pricing_Data_Model.jpg?raw=true)

The main goal of this project was to look at measuring performance focused on Equity returns. As we did with pricing, we can focus on Yearly, Quarterly, Monthly and Daily Returns. We had previously explored this in the project using Python code so rather than going down a long and complex path with DAX, we can use **Python** in **Power Query** to create some tables. 

## *Equity_Returns_by_Year* table

We'll start with the Yearly Returns and create a table called *Equity_Returns_by_Year* by duplicating the *Equity_Prices* table in Power Query and keeping only the *Date*, *Ticker_ID* and *Close* columns. Next, we can click on the *Transform* menu and then *Run Python script* to transform the data into Yearly Returns. When working with pandas, the default pandas dataframe is called *dataset*. We will calculate the *% Return* and the *Cumulative % Return* using log returns by Ticker_ID and Year like what we did independently earlier on the project.

### *[Equity_Returns_by_Year_Python_Code.txt](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Power_BI-Equity-Data-Model-Development/Equity_Returns_by_Year_Python_Code.txt)*  

	# 'dataset' holds the input data for this script
 
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

![Power_BI_Power_Query_Yearly_Equity_Return_Transformation.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Power_Query_Yearly_Equity_Return_Transformation.jpg?raw=true)

The Power Query transformations are similar for the next 3 tables *Equity_Returns_by_Quarter*, *Equity_Returns_by_Month* and *Equity_Returns*.

## *Equity_Returns_by_Quarter* table

### *[Equity_Returns_by_Quarter_Python_Code.txt](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Power_BI-Equity-Data-Model-Development/Equity_Returns_by_Quarter_Python_Code.txt)*

![Power_BI_Power_Query_Quarterly_Equity_Return_Transformation.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Power_Query_Quarterly_Equity_Return_Transformation.jpg?raw=true)

## *Equity_Returns_by_Month* table

### *[Equity_Returns_by_Month_Python_Code.txt](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Power_BI-Equity-Data-Model-Development/Equity_Returns_by_Month_Python_Code.txt)*

![Power_BI_Power_Query_Monthly_Equity_Return_Transformation.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Power_Query_Monthly_Equity_Return_Transformation.jpg?raw=true)

## *Equity_Returns* table

### *[Equity_Returns_Python_Code.txt](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Power_BI-Equity-Data-Model-Development/Equity_Returns_Python_Code.txt)*

![Power_BI_Power_Query_Equity_Return_Transformation.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Power_Query_Equity_Return_Transformation.jpg?raw=true)


## *Equity_Statistics* table

The final table we will create will contain various performance statistics by Ticker for the latest date in a table called *Equity_Statistics. We will use **Python** code in **Power Query** to calculate these metrics. Essentially, we will reference the *Equity_Returns* table in Power Query and then aggregate the dataframe *dataset* as *dataset_stats* for the full time series by *Ticker_ID*. The fields that are calculated in *dataset_stats* are The fields we will calculate are *% Return*, *Cumulative % Return*, *Lowest % Return*, *25th Percentile % Return*, *Median % Return*, *75th Percentile % Return*, *Highest % Return*, *Average % Return*, *Return % Variance*, *Annualized % Return*, *Annualized Volatility* and *Annualized_Downside_Volatility*. *dataset_stats* will be merged to *dataset* by *Ticker_ID* and then the last date will be kept. A new dataframe *dataset_filtered* will be extracted for the last 3 years of data by *Ticker_ID*. 
We compute the *Max % Drawdown* by *Ticker_ID* and the *Calmar Ratio* = *Annualized % Return / Max % Drawdown* and keep the last date. *dataset_filtered* is then merged to *dataset*. Finally, *Annualized Sharpe Ratio* is computed as *(Annualized % Return - risk free rate) / Annualized Volatility* and *Annualized Sortino Ratio* is computed as *(Annualized % Return' - risk free rate) / Annualized Downside Volatility*. Lastly, values are rounded off in the dataframe *dataset*.

### *[Equity_Statistics_Python_Code.txt](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Power_BI-Equity-Data-Model-Development/Equity_Statistics_Python_Code.txt)*

	# 'dataset' holds the input data for this script

	import pandas as pd
	import numpy as np

	# Converting the 'Date' column in 'dataset' to datetime format; invalid parsing will be set to NaT
	dataset['Date'] = pd.to_datetime(dataset['Date'], errors='coerce')

	# Sorting the dataset by 'Ticker_ID' and 'Date' to prepare for analysis
	dataset.sort_values(by=['Ticker_ID', 'Date'], inplace=True)

	# Creating a summary statistics DataFrame by grouping data by 'Ticker_ID'
	dataset_stats = dataset.copy().groupby('Ticker_ID').agg(
    		Lowest_Return=('% Return', 'min'),  # Minimum % Return for each ticker
    		Percentile_25=('% Return', lambda x: x.quantile(0.25)),  # 25th percentile % Return
    		Median_Return=('% Return', 'median'),  # Median % Return
    		Percentile_75=('% Return', lambda x: x.quantile(0.75)),  # 75th percentile % Return
    		Highest_Return=('% Return', 'max'),  # Maximum % Return
    		Average_Return=('% Return', 'mean'),  # Average % Return
    		Return_Variance=('% Return', lambda x: x.std(ddof=0)),  # Variance of % Return
    		Annualized_Return=('% Return', lambda x: (1 + x).prod() ** (252 / x.count()) - 1),  # Annualized % Return
    		Annualized_Volatility=('% Return', lambda x: x.std(ddof=0) * np.sqrt(252)),  # Annualized Volatility
    		Annualized_Downside_Volatility=('% Return', lambda x: x[x < 0].std(ddof=0) * np.sqrt(252) if len(x[x < 0]) > 0 else 0)  # Annualized Downside Volatility
	).reset_index()  # Resetting the index to keep 'Ticker_ID' as a column

	# Renaming the columns for better readability
	dataset_stats.rename(columns={
    		'Lowest_Return': 'Lowest % Return',
    		'Percentile_25': '25th Percentile % Return',
    		'Median_Return': 'Median % Return',
    		'Percentile_75': '75th Percentile % Return',
    		'Highest_Return': 'Highest % Return',
    		'Average_Return': 'Average % Return',
    		'Return_Variance': 'Return % Variance',
    		'Annualized_Return': 'Annualized % Return',
    		'Annualized_Volatility': 'Annualized Volatility',
   		 'Annualized_Downside_Volatility': 'Annualized Downside Volatility'
	}, inplace=True)

	# Merging the summary statistics back into the original dataset based on 'Ticker_ID'
	dataset = dataset.merge(dataset_stats, on='Ticker_ID', how='left')

	# Creating a copy of the dataset where 'Date' is not null for further analysis
	dataset_stats = dataset[dataset['Date'].notnull()].copy()

	# Updating 'dataset' to only keep the non-null dates
	dataset = dataset_stats

	# Sorting the dataset again by 'Ticker_ID' and 'Date'
	dataset.sort_values(by=['Ticker_ID', 'Date'], inplace=True)

	# Deleting the temporary dataset_stats variable to free up memory
	del dataset_stats

	# Finding the last date in the dataset
	last_date = dataset['Date'].max()

	# Calculating the date three years ago from the last date
	three_years_ago = last_date - pd.DateOffset(days=365 * 3)

	# Filtering the dataset to include only rows from the last three years
	date_filter = (dataset['Date'] >= three_years_ago)
	dataset_filtered = dataset.loc[date_filter].copy()

	# Calculating the peak of the 'Cumulative % Return' for each 'Ticker_ID'
	dataset_filtered['Peak'] = dataset_filtered.groupby('Ticker_ID')['Cumulative % Return'].cummax()

	# Calculating the drawdown based on the peak value
	dataset_filtered['Drawdown'] = np.where(
	    dataset_filtered['Cumulative % Return'] >= 0,
 	    dataset_filtered['Peak'] - dataset_filtered['Cumulative % Return'],
	    dataset_filtered['Peak'] + abs(dataset_filtered['Cumulative % Return'])
	)

	# Calculating the percentage drawdown
	dataset_filtered['% Drawdown'] = np.where(
	    dataset_filtered['Peak'] != 0,
	    round((dataset_filtered['Drawdown'] / dataset_filtered['Peak']), 2),
	    0
	)

	# Calculating the maximum percentage drawdown for each ticker
	dataset_filtered['Max % Drawdown'] = dataset_filtered.groupby('Ticker_ID')['% Drawdown'].transform('max')

	# Extracting the last dates for each ticker
	dataset_filtered_last_dates = dataset_filtered.loc[dataset_filtered.groupby('Ticker_ID')['Date'].idxmax()]

	# Calculating the Calmar Ratio for each ticker
	dataset_filtered_last_dates['Calmar Ratio'] = np.where(
	    dataset_filtered_last_dates['Max % Drawdown'] == 0,
	    0,  # Avoid division by zero
	    dataset_filtered_last_dates['Annualized % Return'] / dataset_filtered_last_dates['Max % Drawdown']
	)

	# Updating the dataset to only include the last date entries
	dataset_filtered = dataset_filtered_last_dates

	# Deleting the temporary dataset_filtered_last_dates variable to free up memory
	del dataset_filtered_last_dates
	
	# Selecting only relevant columns for the final dataset
	dataset_filtered = dataset_filtered[['Ticker_ID', 'Max % Drawdown', 'Calmar Ratio']]

	# Extracting the last dates for each ticker from the original dataset
	dataset_last_dates = dataset.loc[dataset.groupby('Ticker_ID')['Date'].idxmax()]

	# Updating the dataset to only include the last date entries
	dataset = dataset_last_dates

	# Deleting the temporary dataset_last_dates variable to free up memory
	del dataset_last_dates

	# Setting a risk-free rate for financial calculations
	risk_free_rate = 0.025

	# Calculating the Annualized Sharpe Ratio for each ticker
	dataset['Annualized Sharpe Ratio'] = np.where(
	    dataset['Annualized Volatility'] == 0,
	    0,  # Avoid division by zero
	    (dataset['Annualized % Return'] - risk_free_rate) / dataset['Annualized Volatility']
	)

	# Calculating the Annualized Sortino Ratio for each ticker
	dataset['Annualized Sortino Ratio'] = np.where(
	    dataset['Annualized Volatility'] == 0,
	    0,  # Avoid division by zero
	    (dataset['Annualized % Return'] - risk_free_rate) / dataset['Annualized Downside Volatility']
	)

	# Merging the filtered dataset back into the main dataset based on 'Ticker_ID'
	dataset = dataset.merge(dataset_filtered, on='Ticker_ID', how='left')

	# Deleting the temporary dataset_filtered variable to free up memory
	del dataset_filtered

	# Rounding specific columns to improve readability
	columns_to_round = [
	    "25th Percentile % Return",
 	    "Median % Return",
  	    "75th Percentile % Return",
  	    "Average % Return",
  	    "Return % Variance",
 	    "Annualized % Return",
	    "Annualized Volatility",
	    "Annualized Downside Volatility",
	    "Max % Drawdown"
	]
	dataset[columns_to_round] = dataset[columns_to_round].round(4)  # Rounding to 4 decimal places

	# Rounding additional columns for improved readability
	columns_to_round2 = [
	    "Annualized Sharpe Ratio",
 	    "Annualized Sortino Ratio",
 	    "Calmar Ratio"
	]
	dataset[columns_to_round2] = dataset[columns_to_round2].round(2)  # Rounding to 2 decimal places

The dataframe *dataset* is returned as a table and after a few more cleanup steps in Power Query, we have the final table called *Equity_Statistics*.

![Power_BI_Power_Query_Equity_Statistics_Transformation.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Power_Query_Equity_Statistics_Transformation.jpg?raw=true)

We'll add a measure to rank Annualized Return by Sector. We'll copy the *Sector_ID* column from the *Sectors* table to *Equity_Statistics*. We use the **DAX** **RANK** function as a dense rank using *Annualized % Return* and *Sector_ID* from the *Equity_Statistics* table.

	Sector_ID = RELATED(Sectors[Sector_ID])

	RankAnnualizedReturnsbySector = 
	RANK(DENSE, 
    	     ORDERBY('Equity_Statistics'[Annualized % Return], DESC),
             PARTITIONBY('Equity_Statistics'[Sector_ID])
	)

And lastly, we'll add another measure to rank Annualized Return by Sub-Industry. We'll copy the *Sub_Industry_ID* column from the *Sub_Industries* table to *Equity_Statistics*. We use the **DAX** **RANK** function as a dense rank using *Annualized % Return* and *Sub_Industry_ID* from the *Equity_Statistics* table.

	Sub_Industry_ID = RELATED(Sub_Industries[Sub_Industry_ID])

	RankAnnualizedReturnsbySub_Industry = 
	RANK(DENSE, 
    	     ORDERBY('Equity_Statistics'[Annualized % Return], DESC),
    	     PARTITIONBY('Equity_Statistics'[Sub_Industry_ID])
 	)

Now, we create new relationships to the performance tables that we created. We'll create a **one-to-many relationship** between *Ticker_ID* in the *Equities* table to *Ticker_ID* in the *Equity_Returns_by_Year*, *Equity_Returns_by_Quarter*, *Equity_Returns_by_Month*, *Equity_Returns* and *Equity_Statistics* tables.

![Power_BI_Return_Data_Model_Relationships.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Return_Data_Model_Relationships.jpg?raw=true)

And our final Data Model now looks like this:

![Power_BI_Final_Data_Model.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Final_Data_Model.jpg?raw=true)

