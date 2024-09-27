
Let's do the same type of analysis we did using SQL in Python. We will adding new functions to our *custom_python_functions.py* file which can be re-used in this project. 

## Modify custom re-usable functions: *[custom_python_functions.py](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Custom-Python-Functions/custom_python_functions.py)*

We'll start by defining a pricing function called *get_pricing_data* that will take a daily pricing dataframe and period type such as *Year*, *Quarter* or *Month* as parameters. The dataframe data retrieved is similar to the data coming from the Yearly pricing or Quarterly pricing views we created in SQL.

    def get_pricing_data(df_tmp, period):
    
        """
        This function processes pricing data from a DataFrame based on the specified period ('Year', 'Quarter', or 'Month').
    
        Parameters:
        - df_pricing: DataFrame containing the pricing data.
        - period: String specifying the period for aggregation ('Year', 'Quarter', or 'Month').

        Returns:
        - Processed DataFrame aggregated by the specified period.
        """
    
      
        # Conditionally add the period column based on the specified period
        if period == 'Quarter':
            df_tmp['Quarter'] = df_tmp['Date'].dt.quarter
            required_cols = ['Ticker', 'Year', 'Quarter']
        elif period == 'Month':
            df_tmp['Month'] = df_tmp['Date'].dt.month
            required_cols = ['Ticker', 'Year', 'Month']
        else:  # Default to 'Year'
            required_cols = ['Ticker', 'Year']
        
        # Group data by required_cols, aggregating relevant columns
        df_tmp2 = df_tmp.groupby(required_cols).agg(
            {
                'Date': 'last',   # Get the last date for each group
                'Open': "first",  # Get the first opening price for each group
                'High': 'max',    # Get the maximum high price for each group
                'Low': 'min',     # Get the minimum low price for each group
                'Close': 'last',  # Get the last closing price for each group
                'Volume': 'last'  # Get the last volume for each group
            }
        ).reset_index()  # Reset the index to make 'Ticker' and 'Year' columns

        # Return the processed DataFrame
        return df_tmp2

We'll also want to plot **Candlestick Charts** of pricing data and to do that, you'll need to have the **plotly** package installed. We'll use the plotly.io module for handling the output which we will set to render to the web browser by default. For more on Candlestick Charts, refer to this link: [Candlestick Chart Definition and Basics Explained](https://www.investopedia.com/terms/c/candlestick.asp). Let's define a function called *plot_pricing_candlestick* which takes a daily pricing dataframe, Ticker name and period type as parameters.

     import plotly as pltly
     import plotly.io as pio
     pio.renderers.default='browser'

     def plot_pricing_candlestick(df_tmp, ticker, period):
     
        """
        Plots a candlestick chart for the given DataFrame, ticker, and period.
    
        Parameters:
        - df_tmp: DataFrame containing pricing data with 'Date', 'Open', 'High', 'Low', 'Close'.
        - ticker: The stock ticker symbol.
        - period: The period type for the x-axis ticks ('Year', 'Quarter', 'Month, or 'Daily').
        """
    
        # Generate tick_text based on the period
        if period == 'Year':
            tick_text = [date.strftime('%Y-%m-%d') + " (" + date.strftime('%Y') + ")" for date in df_tmp['Date']]
        elif period == 'Quarter':
            tick_text = [date.strftime('%Y-%m-%d') + " (" + date.strftime('%Y') + "-Q" + str(quarter) + ")" 
                     for date, quarter in zip(df_tmp['Date'], df_tmp['Quarter'])]
        elif period == 'Month':
            tick_text = [date.strftime('%Y-%m-%d') + " (" + date.strftime('%B') + ")" for date in df_tmp['Date']]
        else:
            tick_text = [date.strftime('%Y-%m-%d') for date in df_tmp['Date']]
        
        if period == 'Daily':
            period = ''
            width_size = 1900
            height_size = 900
        else:
            period = period + ' '
            width_size = 800
            height_size = 600
              
        # Plot the candlestick chart using Plotly
        fig = pltly.graph_objects.Figure(data=[pltly.graph_objects.Candlestick(
            x=df_tmp['Date'],
            open=df_tmp['Open'], 
            high=df_tmp['High'],
            low=df_tmp['Low'], 
            close=df_tmp['Close'], name=ticker)])
    
        # Update layout of the candlestick chart
        fig.update_layout(
            title=f"{ticker} {period}Price Chart",
            xaxis_title="Date",
            yaxis_title="Close Price",
            xaxis_rangeslider_visible=False,
            xaxis=dict(
                tickvals=df_tmp['Date'],
                ticktext=tick_text  # No need for additional list
            ),
            width=width_size,
            height=height_size
        )
        fig.show()

Let's define a function called *plot_pricing_candlestick* takes a daily pricing dataframe, Ticker name and period type as parameters. Next we'll define a function called *plot_pricing_line* to create a **Line Chart** using the **matplotlib** package. It also takes a daily pricing dataframe, Ticker name and period type as parameters but also a price type.

        import matplotlib.pyplot as plt
        
        def plot_pricing_line(df_tmp, ticker, period, price):

            """
            Plots a line chart for the given DataFrame, ticker, and period.

            Parameters:
            - df_tmp: DataFrame containing pricing data (e.g., with 'Date', 'Open', 'High', 'Low', 'Close').
            - ticker: The stock ticker symbol.
            - period: The period type for the x-axis ('Year', 'Quarter', 'Month', or 'Daily').
            - price: The column name for the y-axis values to plot (e.g., 'Close', 'Open').

            This function creates a simple line chart for a given financial asset 
            over the specified period, with properly formatted x and y axis labels, 
            a grid, and rotated x-axis labels for better readability.
            """

            # Check if the period is 'Daily'
            if period == 'Daily':
                x = 'Date'
                period = ''
                label = x
            # If period is not 'Daily', use the period itself for the x-axis
            else:
                x = period
                label = period
                period = period + ' '


            # Create a line chart
            plt.plot(df_tmp[x], df_tmp[price])
    
            # Adding title and labels
            plt.title(f"{ticker} {period}Price Chart")
            plt.xlabel(label)
            plt.ylabel(price)
    
            # Show the plot
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.xticks(rotation=45)  # Rotate x-axis labels for better readability if necessary
            plt.show()

In order to calculate returns, we define a function called *calculate_return* which takes a daily pricing dataframe and period type as parameters and returns a dataframe with Ticker returns. 

    def calculate_return(df_tmp, period):

        """
        Calculate the return percentage based on the 'Close' and 'Open' prices for a given period type.
    
        Parameters:
        - df_tmp: The DataFrame containing the historical data.
        - period: A string indicating the period ('Year', 'Quarter', 'Month', or 'Daily').

        Returns:
        - A DataFrame with a new column '% Return' containing the percentage return, or None if not applicable.
        """
        # Shift the 'Close' prices by 1 for the entire DataFrame
        df_tmp['Prev_Close'] = df_tmp.groupby('Ticker')['Close'].shift(1)
    
        # Get Min Date for Ticker
        df_tmp['Min_Date'] = df_tmp.groupby('Ticker')['Date'].transform('min')

        # Create a condition for the first Date (based on the provided period)
        is_first_period = (df_tmp['Date'] == df_tmp['Min_Date'])
    
        # Initialize the return column
        df_tmp['% Return'] = 0

        # Calculate the return for the first period based on 'Open' and 'Close'
        df_tmp.loc[is_first_period, '% Return'] = round(((df_tmp['Close'] / df_tmp['Open']) - 1.0) * 100, 2)
    
        # Calculate the return for subsequent periods based on the previous close price
        same_ticker = df_tmp['Ticker'] == df_tmp['Ticker'].shift(1)
        df_tmp.loc[~is_first_period & same_ticker, '% Return'] = round(((df_tmp['Close'] / df_tmp['Prev_Close']) - 1.0) * 100, 2)

        # Drop the 'Min_Date' and 'Prev_Close' columns after calculation if not needed
        df_tmp.drop(columns=['Min_Date', 'Prev_Close'], inplace=True)
    
        # Rename the % Return column based on period type
        if period != 'Daily':
            df_tmp.rename(columns={'% Return': period + ' % Return'}, inplace=True)    
    
        return df_tmp

        

        
## Equity Yearly Pricing Analysis: *[Equity-Yearly-Pricing-Analysis.ipynb](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-Equity-Performance-Analysis/Equity-Yearly-Pricing-Analysis.ipynb)*

Let's connect to the database, store the yearly pricing data in the dataframe, get the yearly pricing data for **MSFT**, print the results and plot the Candlestick chart.

        # Define SQL query to retrieve tickers from the Yahoo_Equity_Prices table
        sql_stat = """SELECT 
                TRIM(q2.Ticker) AS Ticker,
                q1.Date,
                ROUND(q1.[Open], 2) AS "Open",
                ROUND(q1.[High], 2) AS "High",
                ROUND(q1.[Low], 2) AS "Low",
                ROUND(q1.[Close], 2) AS "Close",
                q1.Volume AS "Volume"
        FROM [Financial_Securities].[Equities].[Yahoo_Equity_Prices] q1
        INNER JOIN [Financial_Securities].[Equities].[Equities] q2
        ON q1.Ticker_ID = q2.Ticker_ID
        ORDER BY q2.Ticker, q1.Date
        """

        try:
            # Execute the SQL query and read the results into a DataFrame
            df_pricing = pd.read_sql(sql_stat, s1.bind)
    
        except sa.exc.SQLAlchemyError as e:
            # Handle exceptions during SQL query execution
            print(f"Issue querying database tables! Error: {e}")
            s1.close()
            raise

        if df_pricing.empty:
            print("DataFrame is empty after SQL query.")
    
        else:
            df_pricing['Date'] = pd.to_datetime(df_pricing['Date'])
            df_pricing['Year'] = df_pricing['Date'].dt.year
            df_pricing.sort_values(by=['Ticker', 'Date'], inplace=True)

            # Default Ticker used in single ticker analysis
            ticker = 'MSFT'

            df_pricing_yr = get_pricing_data(df_pricing, 'Year') 
            df_pricing_yr_ticker = df_pricing_yr[df_pricing_yr['Ticker'] == ticker].copy()
            df_pricing_yr_ticker.sort_values(by=['Date'], inplace=True)

            # Print yearly pricing data
            print(df_pricing_yr_ticker.to_string(index=False))

            plot_pricing_candlestick(df_pricing_yr_ticker, ticker, 'Year')

       s1.close() 

 ![MSFT_Yearly_Pricing_Data_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Yearly_Pricing_Data_Python.jpg?raw=true)

 ![MSFT_Yearly_Pricing_Candlestick_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Yearly_Pricing_Candlestick_Chart.jpg?raw=true)

What we can observe here is that **MSFT** has a positive trend overall from 2021 to 2024. IF we look at 2021, the candle is green, and the body of the candle is close to the wick ends which indicates that the Close prices were not far off the lowest price and highest price of the year. The top of the candle body (Close price) is further from the wick top (High price) than the body bottom (Open price) is from the wick bottom (Low price) could mean that price was declining at some point and possible at end of 2021. The decline in 2021 could very well be the case as the candle in 2022 was red and the Open vas very close to the High price. In general, **MSFT** Close had a substantial increase in 2021 and a substantial decrease in 2022 where it declined almost as much. 2023 was a good year and 2024 was positive but appears to have had a decline as the top wick takes up most of the candle indicating that the Close has fallen off far from the High of the year.

Now let’s look at the daily Close prices for **MSFT** to get a more granular picture. Let's call the *plot_pricing_line* function we defined.

      df_pricing_daily_ticker = df_pricing[df_pricing['Ticker'] == ticker].copy() 
      plot_pricing_line(df_pricing_daily_ticker, ticker, 'Daily', 'Close')

 ![MSFT_Daily_Pricing_Line_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Daily_Pricing_Line_Chart.jpg?raw=true)

We can see that **MSFT** has a positive trend with a smaller positive trend in 2021, a negative trend in 2022, and longer positive trend from 2023 to 2024. In 2021, it looks like **MSFT** declined from its peak in November of 2021 as we speculated in our earlier observation of the 2021 Yearly price candle. Let’s filter the data further for the last 2 months of 2021 and call the *plot_pricing_line* function again.

     date_filter = (df_pricing_daily_ticker['Date'] >= '2021-11-01') & (df_pricing_daily_ticker['Date'] <= '2021-12-31')
     df_pricing_daily_ticker = df_pricing_daily_ticker.loc[date_filter]
     plot_pricing_line(df_pricing_daily_ticker, ticker, 'Daily', 'Close')

![MSFT_Daily_Pricing_Line_Chart_2021_last_2_months.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Daily_Pricing_Line_Chart_2021_last_2_months.jpg?raw=true)

Here we clearly see that the **MSFT** declined from its peak, had 2 attempts at reaching its highest price and then started its decline into 2022.



            





