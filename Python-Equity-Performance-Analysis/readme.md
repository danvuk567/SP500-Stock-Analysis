
Let's do the same type of analysis we did using SQL in Python. To do that, we'll define a pricing function called *get_pricing_data* that will take a daily pricing dataframe and period type such as *Year*, *Quarter* or *Month*. The data retrieved is similar to the data coming from the Yearly pricing or Quarterly pricing views we created in SQL. We will add this to *custom_python_functions.py* which can be re-used in this project. We'll also plot **Candlestick** charts of pricing data and to do that, you'll need to have the plotly package installed. We'll use the plotly.io module for handling the output which we will set to render to the web browser by default. For more on Candlestick Charts, refer to this link: [Candlestick Chart Definition and Basics Explained](https://www.investopedia.com/terms/c/candlestick.asp)

## Modify custom re-usable functions: *[custom_python_functions.py](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Custom-Python-Functions/custom_python_functions.py)*

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
        
## Equity Year Prices Query: *[Equity-Year-Prices-Query.ipynb](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-Equity-Perfromance-Analysis/Equity-Year-Prices-Query.ipynb)*

Let's connect to the database, store the yearly pricing data in the dataframe, get the yearly pricing data for **MSFT*, print the results and plot the Candlestick chart.

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

            





