
Let's do the same type of analysis we did using SQL in Python. To do that, we'll define a pricing function called *get_pricing_data* that will take a daily pricing dataframe and period type such as *Year*, *Quarter* or *Month*. The data retrieved is similar to the data coming from the Yearly pricing or Quarterly pricing views we created in SQL. We will add this to custom_python_functions.py which can be re-used in this project.

## Modify custom re-usable functions: *[custom_python_functions.py](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Custom_Python_Functions/custom_python_functions.py)*

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

    



