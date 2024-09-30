
Let's do the same type of analysis we did using SQL in Python. We will adding new functions to our *custom_python_functions.py* file which can be re-used in this project. 

## Modify custom re-usable functions: *[custom_python_functions.py](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Custom-Python-Functions/custom_python_functions.py)*

We'll start by defining a pricing function called *get_pricing_data* that will take a daily pricing dataframe and period type such as *Year*, *Quarter* or *Month* as input parameters. The dataframe data retrieved is similar to the data coming from the Yearly pricing or Quarterly pricing views we created in SQL. We use the built-in *groupby* and *agg* functions we can apply to dataframes to retrieve the **'Date'**, **'Open'**, **'High'**, **'Low'**, **'Close'** and **'Volume'**. 

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

We'll also want to plot **Candlestick Charts** of pricing data and to do that, you'll need to have the **plotly** package installed. We'll use the plotly.io module for handling the output which we will set to render to the Jupyter notebook by default. For more on Candlestick Charts, refer to this link: [Candlestick Chart Definition and Basics Explained](https://www.investopedia.com/terms/c/candlestick.asp). Let's define a function called *plot_pricing_candlestick* which takes a daily pricing dataframe, Ticker name and period type as input parameters.

     import plotly as pltly
     import plotly.io as pio
     pio.renderers.default='notebook_connected'

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

Next we'll define a function called *plot_pricing_line* to create a **Line Chart** using the **matplotlib** package. It also takes a pricing dataframe, Ticker name and period type as input parameters as well as a price type.

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

In order to calculate **Returns**, we define a function called *calculate_return* which takes a daily pricing dataframe and period type as input parameters and returns a dataframe with Ticker returns. We retrieve the number of periods as *no_of_periods* based on the period type. We will first derive the previous Close column for each Ticker. We then calculate the return as (Close / Open) – 1.0 for cases where we have the 1st period where previous Close is null, otherwise we use (Close / Prev Close) – 1.0.

We also use **Log Returns**, aggregate them and de-normalize them to calculate **Cumulative Returns**. For more information on log returns, refer to this link: [What Are Logarithmic Returns and How to Calculate Them in Pandas Dataframe](https://saturncloud.io/blog/what-are-logarithmic-returns-and-how-to-calculate-them-in-pandas-dataframe/). We use the same logic as simple returns to calculate log returns. We then drop the previous Close column, the Log Return column, and the Cumulative Log Return column, and modify the return and cumulative return labels based on period type. We import the *numpy* package to use the *exp* function to de-normalize the aggregate log returns. 

We will also annualize simple returns by using a variation of this basic formula: **(1 + Return) ^ (1 / N) - 1 for N periods**. This gives us an idea of what the compounded returns would be per year. For more information on **Annualized Returns**, refer to this link: [Annualized Total Return Formula and Calculation](https://www.investopedia.com/terms/a/annualized-total-return.asp). In our code, we will divide the *no_of_periods* by the return count for each Ticker. This will give us 1 / N for N years. For example, if we have daily data, we usually have 252 trading days per year and for say 3 years, we will have 252 * 3 returns, and so 252 / (252 * 3) is the same as 1 / 3.

A measure that defines risk with respect to returns is volatility. For more information about volatility, refer to this link: [Volatility: Meaning in Finance and How It Works With Stocks](https://www.investopedia.com/terms/v/volatility.asp) We can define **Annualized Volatility** as **Standard Deviation of Returns * N for N periods**. For downside risk, we can calculate **Downside Annualized Volatility** as **Standard Deviation of Negative Returns * N for N periods**. 

Lastly, we convert our returns and volatility measures into percentages, drop the unwanted columns and return the dataframe with returns data.

    import numpy as np
    
    def calculate_return(df_tmp, period):

        """
        Calculate the return percentage based on the 'Close' and 'Open' prices for a given period type.
    
        Parameters:
        - df_tmp: The DataFrame containing the historical data.
        - period: A string indicating the period ('Year', 'Quarter', 'Month', or 'Daily').

        Returns:
        - A DataFrame with a new column '% Return' containing the percentage return, or None if not applicable.
        """

        # Assign the number of periods based on period type
        if period == 'Year':
            no_of_periods = 1
        elif period == 'Quarter':
            no_of_periods = 4
        elif period == 'Month':
            no_of_periods = 12
        else:
            no_of_periods = 252
        
        # Shift the 'Close' prices by 1 for the entire DataFrame
        df_tmp['Prev_Close'] = df_tmp.groupby('Ticker')['Close'].shift(1)

        # Create a condition for the first period where Prev_Close is NaN
        is_first_period = df_tmp['Prev_Close'].isna()
    
        # Initialize the return column
        df_tmp['% Return'] = 0

        # Calculate % Return for the first period where 'Prev_Close' is NaN
        # Assuming the return is calculated based on 'Close' and 'Open' for these rows
        df_tmp.loc[is_first_period, '% Return'] = ((df_tmp['Close'] / df_tmp['Open']) - 1.0)
    
        # Calculate the return for subsequent periods based on the previous close price
        same_ticker = df_tmp['Ticker'] == df_tmp['Ticker'].shift(1)
        df_tmp.loc[~is_first_period & same_ticker, '% Return'] = ((df_tmp['Close'] / df_tmp['Prev Close']) - 1.0)

        # Calculate the log return for the first period based on 'Open' and 'Close'
        df_tmp.loc[is_first_period, 'Log Return'] = np.log(df_tmp['Close'] / df_tmp['Open']) 
        
        # Calculate the log return for subsequent periods based on the previous close price
        df_tmp.loc[~is_first_period & same_ticker, 'Log Return'] = np.log(df_tmp['Close'] / df_tmp['Prev Close'])
    
        # Calculate the cumulative log return
        df_tmp['Cumulative Log Return'] = df_tmp.groupby('Ticker')['Log Return'].cumsum()
    
        # De-nomralize cumulative log returns
        df_tmp['Cumulative % Return'] = (np.exp(df_tmp['Cumulative Log Return']) - 1.0)

        # Calculate the Cumulative Simple Return
        df_tmp['Cumulative Simple % Return'] = (1 + df_tmp['% Return']).groupby(df_tmp['Ticker']).cumprod() - 1

        # Calculate the rolling count of returns by Ticker for each date using groupby and rolling together
        df_tmp['Rolling Return Count'] = df_tmp.groupby('Ticker')['% Return'].expanding(min_periods=1).count().reset_index(level=0, drop=True)

        # Calculate the Annualized % Return based on Cumulative Simple Return
        df_tmp['Annualized % Return'] = ((1 + df_tmp['Cumulative Simple % Return'])**(no_of_periods / df_tmp['Rolling Return Count']) - 1.0)

        # Calculate the Annualized Volatility based on Simple Return
        df_tmp['Annualized Volatility'] = df_tmp.groupby('Ticker')['% Return'].transform(lambda x: x.std() * np.sqrt(no_of_periods))
    
        # Calculate Downside Annualized Volatility based on Negative Simple Return
        df_tmp['Downside Annualized Volatility'] = df_tmp.groupby('Ticker')['% Return'].transform(lambda x: x[x < 0].std() * np.sqrt(no_of_periods) if not x[x < 0].empty else 0)

        # Convert Returns to percentages
        df_tmp['% Return'] = round(df_tmp['% Return'] * 100, 2)
        df_tmp['Cumulative % Return'] = round(df_tmp['Cumulative % Return'] * 100, 2)
        df_tmp['Annualized % Return'] = round(df_tmp['Annualized % Return'] * 100, 2) 
        df_tmp['Annualized Volatility'] = round(df_tmp['Annualized Volatility'] * 100, 2)
        df_tmp['Downside Annualized Volatility'] = round(df_tmp['Annualized Volatility'] * 100, 2)

        # Drop the 'Prev_Close', 'Log Return', 'Cumulative Log Return', 'Cumulative Simple % Return' and 'Rolling Return Count' columns after calculation
        df_tmp.drop(columns=['Prev Close', 'Log Return', 'Cumulative Log Return', 'Cumulative Simple % Return', 'Rolling Return Count'], inplace=True)
    
        # Rename the Return column based on period type
        if period != 'Daily':
            df_tmp.rename(columns={'% Return': period + ' % Return'}, inplace=True)    
            df_tmp.rename(columns={'Cumulative % Return': period + ' Cumulative % Return'}, inplace=True)
            df_tmp.rename(columns={'Annualized % Return': period + ' Annualized % Return'}, inplace=True)
            df_tmp.rename(columns={'Annualized Volatility': period + ' Annualized Volatility'}, inplace=True)
            df_tmp.rename(columns={'Downside Annualized Volatility': period + ' Downside Annualized Volatility'}, inplace=True)
        
    return df_tmp


Here we define a function called *plot_returns_bar_chart* to create a **Bar Chart** using the **matplotlib** package. It also takes a return dataframe, Ticker name and period type as input parameters as well as a return type.

        def plot_returns_bar_chart(df_tmp, ticker, period, return_type):
    
            """
            Plots a bar chart of returns based on the specified period.
    
            Parameters:
            - df_tmp: DataFrame containing return data.
            - ticker: Stock ticker symbol.
            - period: Time period for x-axis labeling ('Year', 'Quarter', 'Month', etc.).
            """
    
            # Create a Label column based on the period
            if period == 'Year':
                df_tmp['Label'] = df_tmp['Year'].astype(str)
            elif period == 'Quarter':
                df_tmp['Label'] = df_tmp['Year'].astype(str) + "-Q" + df_tmp['Quarter'].astype(str)
            elif period == 'Month':
                # Ensure month is zero-padded if needed
                df_tmp['Label'] = df_tmp['Year'].astype(str) + "-" + df_tmp['Month'].apply(lambda x: str(x).zfill(2))
            else:
                df_tmp['Label'] = df_tmp['Date']
        

            # Check if return_type exists in df_tmp
            if return_type not in df_tmp.columns:
                raise ValueError(f"Column '{return_type}' does not exist in the DataFrame.")
    
            # Plot returns as a bar chart
            colors = ['red' if x < 0 else 'blue' for x in df_tmp[return_type]]
            plt.figure(figsize=(10, 8))
            plt.axhline(0, color='red', linestyle='--', linewidth=2.0)
            plt.bar(df_tmp['Label'], df_tmp[return_type], color=colors, edgecolor='black')
            plt.title(f'{ticker} {return_type}')
            plt.xlabel(period)
            plt.ylabel(return_type)
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.xticks(rotation=45)  # Rotate labels if needed for readability
            plt.show()

Now let's define a function called *calculate_stats* which will calculate Quarterly Return Statistics based on Year and Year % Return. Similar to what we did using SQL queries, we want to find the Lowest, Highest, Average, Median and Variance of Quarterly Returns for each Year. We use the built-in *groupby* and *agg* functions we can apply to dataframes to achieve this. It requires a return dataframe and period type as input parameters and returns a statistics dataframe.

        def calculate_stats(df_ret, period):
    
            """
            Calculate various statistical metrics for returns such as Lowest, Highest, Average, Median returns, 
            and Return Variance for the given period.

            Parameters:
            - df_ret: DataFrame containing return data.
            - period: The period for which the statistics are being calculated ('Year', 'Quarter', 'Month', or 'Daily').

            Returns:
            - df_tmp: A DataFrame containing the calculated statistics for each 'Ticker' over the specified period.
            """
    
            # Determine the required columns based on the given period
            if (period == 'Quarter') or (period == 'Month') or (period == 'Daily'):
                # For these periods, also include 'Year' and 'Year % Return' in the grouping columns
                required_cols = ['Ticker', 'Year', 'Year % Return']
            else:  
                # Default to 'Year' only if the period is not specified as 'Quarter', 'Month', or 'Daily'
                required_cols = ['Ticker']
    
            # Adjust period string for daily returns (no prefix) or for non-daily periods (add space after period)
            if period == 'Daily':
                period = ''  # No period prefix for daily returns
            else:
                period = period + ' '  # Add space to the period to be used as prefix in column names
    
            # Group the data by the required columns and calculate statistical metrics for returns
            df_tmp = df_ret.groupby(required_cols).agg(
                Lowest_Return=(period + '% Return', 'min'),      # Minimum return for the period
                Highest_Return=(period + '% Return', 'max'),     # Maximum return for the period
                Average_Return=(period + '% Return', 'mean'),    # Mean (average) return for the period
                Median_Return=(period + '% Return', 'median'),   # Median return for the period
                Return_Variance=(period + '% Return', lambda x: x.std(ddof=0))  # Variance (standard deviation) of returns
            ).reset_index()  # Reset index to return a DataFrame with a flat structure

            # Round the calculated statistics to 2 decimal places for better readability
            df_tmp = df_tmp.round({
                'Lowest_Return': 2,
                'Highest_Return': 2,
                'Average_Return': 2,
                'Median_Return': 2,
                'Return_Variance': 2
            })

            # Rename the columns to reflect the period and give better clarity
            df_tmp.rename(columns={
                'Lowest_Return': 'Lowest ' + period + '% Return',        # Rename lowest return column
                'Highest_Return': 'Highest ' + period + '% Return',      # Rename highest return column
                'Average_Return': 'Average ' + period + '% Return',      # Rename average return column
                'Median_Return': 'Median ' + period + '% Return',        # Rename median return column
                'Return_Variance': period + '% Variance',                # Rename variance column
            }, inplace=True)
    
            # Return the DataFrame with the calculated statistics
            return df_tmp

This custom function called *plot_year_stats_bar_charts* will use matplotlib subplots to show separate bar charts of each period Statistic based on  *'Year'* and *'Year % Return'* we want to show. The code is a bit tricky and lengthy to get correct dynamic formatting. It requires a statistics dataframe and Ticker name as input parameters.

        def plot_period_stats_by_year_bar_charts(df_stats, ticker):
    
            """
            Create bar charts to visualize various statistics.
    
            Parameters:
            - df_stats: DataFrame containing the combined statistics.
            - ticker: String representing the ticker symbol.
            """
    
            # Determine the columns to plot by excluding 'Ticker' and 'Year'
            columns_to_plot = [col for col in df_stats.columns if col not in ['Ticker', 'Year']]
    
            # Check if there is only one row in the DataFrame
            if len(df_stats) == 1:
        
                # Determine the columns to plot by excluding 'Ticker' and 'Year'
                columns_to_plot = [col for col in df_stats.columns if col not in ['Ticker', 'Year']]
        
                # Extract the single row of statistics
                stats = {col: df_stats[col].values[0] for col in columns_to_plot}
        
                # Create a single subplot
                fig, ax = plt.subplots(figsize=(12, 8))
        
                # Plot each statistic as a bar
                for key, value in stats.items():
                    ax.bar(key, value, color='blue', edgecolor='black', label=key)
        
                ax.set_title(f'{ticker} Year Statistics')
                ax.set_ylabel('Value')
                ax.grid(axis='y', linestyle='--', alpha=0.7)

            else:
        
                # Determine the columns to plot by excluding 'Ticker' and 'Year' and 'Year % Return'
                columns_to_plot = [col for col in df_stats.columns if col not in ['Ticker', 'Year', 'Year % Return']]
        
                # Number of statistics to plot
                num_stats = len(columns_to_plot)
        
                # Determine the grid size based on the number of statistics
                if num_stats <= 4:
                    rows, cols = 2, 2
                elif num_stats <= 6:
                    rows, cols = 3, 2
                elif num_stats <= 9:
                    rows, cols = 3, 3
                else:
                    raise ValueError("Number of statistics exceeds the supported grid size.")
        
                # Create subplots with dynamic grid size
                fig, ax = plt.subplots(rows, cols, figsize=(18, 12))
        
                # Flatten the axes array for easy iteration if it's multidimensional
                ax = ax.flatten()
        
                # Plot each statistic
                for i, col in enumerate(columns_to_plot):
                    # Determine the color based on the return values
                    colors = ['red' if x < 0 else 'blue' for x in df_stats[col]]
            
                    # Plot the bar chart
                    ax[i].bar(df_stats['Year'], df_stats[col], color=colors, edgecolor='black')
                    ax[i].axhline(0, color='red', linestyle='--', linewidth=2.0)
                    ax[i].set_title(f'{ticker} {col}')
                    ax[i].set_xlabel('Year')
                    ax[i].set_ylabel(col)
                    ax[i].grid(axis='y', linestyle='--', alpha=0.7)

                    # Set x-ticks to only whole years
                    ax[i].set_xticks(df_stats['Year'].unique())  # Set x-ticks to unique years
                    ax[i].set_xticklabels(df_stats['Year'].unique().astype(int), rotation=45)  # Use int for tick labels
        
                # Turn off any unused subplots
                for j in range(num_stats, len(ax)):
                    ax[j].axis('off')
        
                # Adjust layout of subplots
                plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1, wspace=0.3, hspace=0.5)

            # Show the plot
            plt.show()


This custom function called *plot_period_returns_by_year_box_plot* will use seaborn to plot **Box Plots**. Box plots are one of my favorite visualizations that tell a lot of the story in numerical data. The boxes themselves represent the interquartile range (IQR), which is the range between the first quartile (Q1, or 25th percentile) and the third quartile (Q3, or 75th percentile). The IQR contains the middle 50% of the data. The Median is a line inside the box represents the median (or second quartile, Q2, or 50th percentile) of the data which is the center of the dataset. The whiskers extend from the edges of the box to the smallest and largest values within 1.5 times the IQR from Q1 and Q3, respectively. Data points that fall outside the whiskers (beyond 1.5 times the IQR from Q1 and Q3) are considered outliers and are typically plotted as individual points.

This function uses the seaborn package to plot the box plots and requires a returns dataframe, Ticker name and period type as input parameters.

        import seaborn as sns
        
        def plot_period_returns_by_year_box_plot(df_ret, ticker, period):
    
            """
            Plots a box plot of returns for a given ticker and period.
    
            Parameters:
            - df_ret: DataFrame containing return data.
            - ticker: Stock ticker symbol.
            - period: Time period for returns (e.g., 'Daily', 'Year', etc.).
            """
    
            # Define properties for outliers in the box plot
            # 'marker' defines the shape of the outliers
            # 'color' sets the color of the outliers
            # 'alpha' adjusts the transparency of the outliers
            # 'markersize' sets the size of the outlier markers
            flierprops = dict(marker='o', color='red', alpha=0.5, markersize=8)

            # Create a figure with a specified size for the plot
            plt.figure(figsize=(12, 8))
    
            # If the period is 'Daily', treat it as an empty string for labeling purposes
            # Otherwise, append a space after the period string for readability in the title
            if period == 'Daily':
                period = ''
            else:
                period = period + ' '

            # Check if the period is 'Year'
            if period == 'Year':
                # If period is 'Year', create a box plot of yearly percentage returns
                # y-axis is set to the 'Year % Return' column in the DataFrame
                sns.boxplot(y=f'Year % Return', data=df_ret, palette="Set2", flierprops=flierprops)
                plt.title(f'{ticker} Year % Returns')  # Title includes the ticker and indicates yearly returns
                plt.ylabel('Year % Return')  # Set the label for the y-axis to 'Year % Return'

            else:
                # For other periods, create a box plot with 'Year' on the x-axis and returns on the y-axis
                # The 'hue' argument differentiates data points by 'Year', using different colors for each year
                sns.boxplot(x='Year', y=f'{period}% Return', data=df_ret, hue='Year', palette="Set2", flierprops=flierprops)
                plt.title(f'{ticker} {period}% Returns by Year')  # Title includes the ticker and period
                plt.xlabel('Year')  # Set the label for the x-axis to 'Year'

            # Add gridlines to the y-axis for clarity, using a dashed line style and slight transparency
            plt.grid(axis='y', linestyle='--', alpha=0.7)

            # Rotate the x-axis labels by 45 degrees for better readability, especially if there are many years
            plt.xticks(rotation=45)
    
            # Display the plot
            plt.show()
            

This function called *plot_top_returns_bar_chart* that uses the plotly package will plot period returns as bar charts within subplots using a plotly color scheme *'Blues'*. This function is quite complex to achive the desired result and format. It uses a pivot function to create a pivot table dataframe that shifts returns under Tickers. It also uses the math package to calculate the number of subplots. It requires a returns dataframe and period type as input parameters.

        import math
        
        def plot_top_returns_bar_chart(df_tmp, period):
        
            """
            Plots a bar chart of returns based on the specified period for multiple tickers.
    
            Parameters:
            - df_tmp: DataFrame containing return data.
            - period: Time period for x-axis labeling ('Year', 'Quarter', 'Month', etc.).
            """
            if period == 'Daily':
                raise ValueError("Too many periods to support number of subplots.")
        
            tickers = df_tmp['Ticker'].unique()

            # Create a Label column based on the period
            if period == 'Year':
                df_tmp['Year'] = df_tmp['Year'].astype(int)
                df_tmp['Label'] = df_tmp['Year']
                df_tmp.sort_values(by='Year', inplace=True)
            elif period == 'Quarter':
                df_tmp['Label'] = df_tmp['Year'].astype(str) + "-Q" + df_tmp['Quarter'].astype(str)
                df_tmp['Quarter'] = df_tmp['Quarter'].astype(int)
                df_tmp.sort_values(by=['Year', 'Quarter'], inplace=True)
            elif period == 'Month':
                df_tmp['Label'] = df_tmp['Month'].apply(lambda x: pd.Timestamp(f'2024-{x}-01').strftime('%b')) + "-" + df_tmp['Year'].astype(str)
                df_tmp['Month'] = df_tmp['Month'].astype(int)
                df_tmp.sort_values(by=['Year', 'Month'], inplace=True)
            else:
                df_tmp['Label'] = df_tmp['Date'].astype(str)
            
            return_type = period + ' % Return'
    
            # Check if return_type exists in df_tmp
            if return_type not in df_tmp.columns:
                raise ValueError(f"Column '{return_type}' does not exist in the DataFrame.")

            unique_periods = df_tmp['Label'].unique()
            num_periods = len(unique_periods)

            # Determine the grid size based on the number of periods
            plots = int(math.sqrt(num_periods)) + (1 if (math.sqrt(num_periods) % 1 != 0) else 0)
    
            if num_periods > 48:
                raise ValueError("Number of periods exceeds the supported grid size.")    
    
            rows, cols = plots, plots
    
            if period == 'Year':
                width_size = 800
                height_size = 600
                horiz_space = 0.15
                vert_space = 0.05
            else:
                width_size = 1900
                height_size = 900
                horiz_space=0.05
                vert_space=0.01
    
            fig = make_subplots(rows=rows, cols=cols, vertical_spacing=vert_space, horizontal_spacing=horiz_space)
    
            # Generate a color scale from dark to light blue
            num_tickers = len(tickers)
            color_scale = px.colors.sequential.Blues
            colors = color_scale[:num_tickers] if num_tickers <= len(color_scale) else color_scale * (num_tickers // len(color_scale) + 1)
    
            num_top_tickers = round(len(df_tmp) / num_periods)
    
            # Loop through each period and plot the returns for all tickers
            for i, period_val in enumerate(unique_periods):
                df_period = df_tmp[df_tmp['Label'] == period_val]
        
                # Create a pivot table dataframe to shift returns under 'Label' column for Tickers
                df_pivot = df_period.pivot(index='Ticker', columns='Label', values=return_type)
        
                # Sort by the first column (the only column in this case) in descending order
                df_pivot = df_pivot.sort_values(by=df_pivot.columns[0], ascending=False)

                # Create a bar chart for each period, showing returns of all tickers
                # Add traces for each ticker with distinct colors
                for j, ticker in enumerate(df_pivot.index):
                    y_values = df_pivot.loc[ticker].values
                    fig.add_trace(
                        pltly.graph_objects.Bar(
                            x=[period_val],  # Use the period value as x-tick for that subplot
                            y=y_values,  # Use the pivoted values
                            name=ticker,
                            marker_color=colors[j % len(colors)],  # Apply color
                            text=ticker,  # Display ticker on bars
                            textposition='inside'  # Label on bars
                        ),
                        row=(i // cols) + 1,
                        col=(i % cols) + 1
                    )
    
            fig.update_layout(
                height=height_size * rows,  # Adjust height based on number of rows
                width=width_size,
                title_text=f'Top {num_top_tickers} Tickers by {period} % Return',
                plot_bgcolor='lightgrey',  # Background color
                paper_bgcolor='white',  # Paper background color
                showlegend=False  # Hide legend
            )
    
            # Update y-axis labels for each subplot
            for i, label in enumerate(unique_periods):
                fig.update_yaxes(title_text=return_type, row=(i // cols) + 1, col=(i % cols) + 1)
    
            fig.show()


This function called *plot_returns_line_chart* will plot simple or cumulative returns in a **Line Chart** using the plotly package for single or multiple Tickers. It requires a returns dataframe, a period type and return type as input parameters. 

        def plot_returns_line_chart(df_tmp, period, return_type):
    
            """
            Plots a line chart for multiple tickers based on the specified period using Plotly.

            Parameters:
            - df_tmp: DataFrame containing return data.
            - period: A string indicating the period ('Year', 'Quarter', 'Month', 'Daily').

            Returns:
            - None
            """
            
            # Create a Label column based on the period
            if period == 'Year':
                df_tmp['Label'] = df_tmp['Year'].astype(str)
            elif period == 'Quarter':
                df_tmp['Label'] = df_tmp['Year'].astype(str) + "-Q" + df_tmp['Quarter'].astype(str)
            elif period == 'Month':
                # Ensure month is zero-padded if needed
                df_tmp['Label'] = df_tmp['Year'].astype(str) + "-" + df_tmp['Month'].apply(lambda x: str(x).zfill(2))
            else:
                df_tmp['Label'] = df_tmp['Date'].astype(str)
        
            if period == 'Daily':
                label = 'Date'
                period = ''
            else:
                label = period

            tickers = df_tmp['Ticker'].unique()
    
            if len(tickers) == 0:
                print("No tickers found in the DataFrame.")
                return
            elif len(tickers) == 1:
                ticker_label = tickers[0]
            else:
                ticker_label = 'Ticker'
    
            if return_type not in df_tmp.columns:
                print(f"Column '{return_type} not found in the DataFrame.")
                return
    
            fig = pltly.graph_objects.Figure()
    
            for ticker in tickers:
                df_ticker = df_tmp[df_tmp['Ticker'] == ticker]
                if df_ticker.empty:
                    print(f"No data found for ticker {ticker}.")
                continue
        
            fig.add_trace(
                pltly.graph_objects.Scatter(
                    x=df_ticker['Label'],
                    y=df_ticker[return_type],
                    mode='lines',
                    name=ticker
                )
            )
    
            fig.update_layout(
                title=f'{return_type} for {ticker_label}',
                xaxis_title=label,
                yaxis_title=f'{return_type}',
                legend_title='Ticker',
                plot_bgcolor='#f5f5f5',  # Lightest grey
                paper_bgcolor='white'
            )
    
            fig.update_xaxes(tickangle=45)  # Rotate x-axis labels for better readability if necessary
            fig.show()

We will now define a function called  *calculate_drawdowns* that will calculate the drawdowns, cumulative max drawdowns (rolling worst drawdown) and maximum drawdown for all dates using cumulative returns based on Ticker. A **Drawdown** is another measure of risk and is the difference between the peak value and the trough value that follows. For more information on drawdowns, refer to this link: [Drawdown: What It Is, Risks, and Examples](https://www.investopedia.com/terms/d/drawdown.asp). Here we simply calculate the drawdown at each date as the difference in cumulative return from the rolling peak cumulative return. We pass the return dataframe as input, the period type and return the same dataframe with drawdown columns for the period: *'Peak'*, *'Drawdown'*, *'% Drawdown'*, *'Cumulative Max % Drawdown'*, *'Max % Drawdown'*, and *'Max Drawdown Date'*.

        def calculate_drawdowns(df_tmp, period):
    
            """
            Calculate drawdowns and maximum drawdown based on cumulative returns.
    
            Parameters:
            - df_tmp: The DataFrame containing the cumulative return data.
            - period: The period type (e.g., 'Daily', 'Monthly', etc.), which is used to label the columns.

            Returns:
            - A DataFrame with new columns for drawdown and maximum drawdown.
            """

            # Determine the label for the columns based on the period type
            if period == 'Daily':
                label = ''
            else:
                label = period + ' '
        
            # Ensure the DataFrame is sorted by Date for proper calculations
            df_tmp.sort_values(by=['Ticker', 'Date'], inplace=True)

            # Check for 'Cumulative % Return' presence
            if label + 'Cumulative % Return' not in df_tmp.columns:
                raise ValueError(f"{label}Cumulative % Return column is missing. Please calculate returns first.")
    
            # Calculate Peak for each Ticker
            df_tmp['Peak'] = df_tmp.groupby('Ticker')['Cumulative % Return'].cummax()
    
            # Calculate Drawdown as the difference between Peak and Cumulative Return
            df_tmp['Drawdown'] = np.where(
                df_tmp[label + 'Cumulative % Return'] >= 0,  # If cumulative return is positive or zero
                df_tmp['Peak'] - df_tmp[label + 'Cumulative % Return'],  # Calculate drawdown normally
                df_tmp['Peak'] + abs(df_tmp[label + 'Cumulative % Return'])  # Account for negative cumulative return
            )
    
            # Calculate % Drawdown
            df_tmp['% Drawdown'] = np.where(
                df_tmp['Peak'] != 0,
                round((df_tmp['Drawdown'] / df_tmp['Peak']) * 100, 2),
                0
            )

            # Calculate Cumulative Max % Drawdown for each Ticker (worst drawdown observed up to each date)
            df_tmp['Cumulative Max % Drawdown'] = df_tmp.groupby('Ticker')['% Drawdown'].cummax()
    
            # Max % Drawdown column represents max drawdown of all dates
            df_tmp['Max % Drawdown'] = df_tmp.groupby('Ticker')['% Drawdown'].transform('max')
            # Create a mask where % Drawdown equals Max % Drawdown
            df_tmp['Is_Max_Drawdown'] = df_tmp['% Drawdown'] == df_tmp['Max % Drawdown']
            # Extract the last date where the Max % Drawdown occurs
            df_tmp['Max Drawdown Date'] = df_tmp['Date'].where(df_tmp['Is_Max_Drawdown']).groupby(df_tmp['Ticker']).transform('last')

            # If the period is not 'Daily', rename the columns with the period label prefix
            if period != 'Daily':
                df_tmp.rename(columns={'Peak': label + 'Peak'}, inplace=True)
                df_tmp.rename(columns={'Drawdown': label + 'Drawdown'}, inplace=True)
                df_tmp.rename(columns={'% Drawdown': label + '% Drawdown'}, inplace=True)
                df_tmp.rename(columns={'Cumulative Max % Drawdown': label + 'Cumulative Max % Drawdown'}, inplace=True)
                df_tmp.rename(columns={'Max % Drawdown': label + 'Max % Drawdown'}, inplace=True)
                df_tmp.rename(columns={'Max Drawdown Date': label + 'Max Drawdown Date'}, inplace=True)

        return df_tmp


## Equity Performance Analysis: *[Equity-Performance-Analysis.ipynb](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-Equity-Performance-Analysis/Equity-Performance-Analysis.ipynb)*

Let's explore the data and do some performance analysis with the custom functions we created within the python code defined in this file. We'll start out by we connecting to the database and store the yearly pricing data in the dataframe *df_pricing*. We raise a ValueError exception if the dataframe is empty. We'll set our default Ticker to be **MSFT** when doing individual equity analysis. We then get the yearly pricing data for **MSFT**, print the results and plot the Candlestick chart.

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
            raise ValueError("DataFrame is empty after SQL query.")

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


Now we call the calculate_return function with a copy of the *df_pricing_yr* dataframe and use *'Year'* as period type to return the *df_yearly_ret* dataframe. We slice the *df_yearly_ret* dataframe for **MSFT** ticker and we print the dataframe without the index for the columns we want to retain.

     df_yearly_ret = calculate_return(df_pricing_yr.copy(), 'Year')
     df_yearly_ret_ticker = df_yearly_ret[df_yearly_ret['Ticker'] == ticker].copy()
     df_yearly_ret_ticker = df_yearly_ret_ticker[['Ticker', 'Year', 'Date', 'Year % Return']]
     print(df_yearly_ret_ticker.to_string(index=False))

 ![MSFT_Yearly_Return_Data_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Yearly_Return_Data_Python.jpg?raw=true)

Let's plot a bar chart of the Yearly returns for **MSFT** using our custom function *plot_returns_bar_chart*.

    plot_returns_bar_chart(df_yearly_ret_ticker, ticker, 'Year', 'Year % Return')

 ![MSFT_Yearly_Return_Bar_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Yearly_Return_Bar_Chart.jpg?raw=true)

Let’s juxtapose the Yearly returns with Quarterly returns. We'll use our custom *get_pricing_data* function for Quarter period and create a new dataframe *df_pricing_qtr* to house Quarterly pricing data. We then derive another dataframe df_pricing_qtr_ticker for **MSFT**.  We’ll then use our custom function *calculate_return* to calculate the return based on Quarterly logic. And then we merge df_yearly_ret with df_quarterly_ret using Ticker and Year and we print the dataframe without the index for the columns we want to retain.

     df_pricing_qtr = get_pricing_data(df_pricing.copy(), 'Quarter')
     df_quarterly_ret = calculate_return(df_pricing_qtr.copy(), 'Quarter')
     df_comb_ret = pd.merge(df_yearly_ret, df_quarterly_ret, on=['Ticker', 'Year'])
     df_comb_ret.rename(columns={'Date_y': 'Date'}, inplace=True)
     df_comb_ret.sort_values(by=['Ticker', 'Year', 'Quarter'], inplace=True)
    
     df_comb_ret_ticker = df_comb_ret[df_comb_ret['Ticker'] == ticker].copy()
     df_comb_ret_ticker = df_comb_ret_ticker[['Ticker', 'Year', 'Year % Return', 'Quarter', 'Date', 'Quarter % Return']]

     print(df_comb_ret_ticker.to_string(index=False))
     
 ![MSFT_Yearly_Return_Quarterly_Return_Data_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Yearly_Return_Quarterly_Return_Data_Python.jpg?raw=true)

Let's plot a bar chart of the Quarterly returns for **MSFT** using the df_comb_ret_ticker dataframe and custom function *plot_returns_bar_chart*.

     plot_returns_bar_chart(df_comb_ret_ticker, ticker, 'Quarter', 'Quarter % Return')

 ![MSFT_Quarterly_Return_Bar_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Quarterly_Return_Bar_Chart.jpg?raw=true)   

Let's call our custom function *calculate_stats* for **MSFT** using the df_comb_ret_ticker dataframe to retrieve the Quarterly return statistics by year and print the results.

     df_comb_stats_ticker = calculate_stats(df_comb_ret_ticker.copy(), 'Quarter')
     print(df_comb_stats_ticker.to_string(index=False))

 ![MSFT_Quarterly_Return_by_Year_Statistics_Data_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Quarterly_Return_by_Year_Statistics_Data_Python.jpg?raw=true) 

 We can plot all the Quarterly return statistics by year using our custom function *plot_year_stats_bar_charts* for **MSFT**.

      plot_period_stats_by_year_bar_charts(df_comb_stats_ticker, 'MSFT')
 
![MSFT_Quarterly_Return_by_Year_Statistics_Bar_Charts.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Quarterly_Return_by_Year_Statistics_Bar_Charts.jpg?raw=true) 

Based on all the Statistics it looks like 2021 was the top consistently trending year. It was showing a positive Lowest Quarterly return where all other years have negatives, the Quarterly Variance of returns was lower for 2021 than in 2023, and Highest Quarterly returns for 2021 was almost as high as 2023. Both Median and Average Quarterly returns were 2nd highest compared to 2023. 

Now let’s explore what happened using monthly returns by year using box plots. We fetch the Monthly returns using our custom functions and then call our custom function *plot_period_returns_by_year_box_plot* to plot the box plot for **MSFT**.

      df_pricing_mth = get_pricing_data(df_pricing.copy(), 'Month')
      df_monthly_ret = calculate_return(df_pricing_mth.copy(), 'Month')
      df_monthly_ret_ticker = df_monthly_ret[df_monthly_ret['Ticker'] == ticker].copy()
      df_monthly_ret_ticker = df_monthly_ret_ticker[['Ticker', 'Year', 'Month', 'Month % Return']]
      plot_period_returns_by_year_box_plot(df_monthly_ret_ticker, ticker, 'Month')

![MSFT_Monthly_Return_by_Year_Box_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/MSFT_Monthly_Return_by_Year_Box_Chart.jpg?raw=true)

Now let’s examine Yearly returns for multiple stocks and get the top 5 performers by year. We will use our *df_yearly_ret* dataframe to create a new column using the *rank* function to rank returns in non-ascending order and cast as an integer. We’ll create a new dataframe called *df_yearly_ret_top* from slicing *df_yearly_ret* by *'Year % Return Rank' <= num_of_ranks* where *num_of_ranks = 5*. We then sort *df_yearly_ret_top* and print the results.

      df_yearly_ret['Year % Return Rank'] = df_yearly_ret.groupby('Year')['Year % Return'].rank(ascending=False, method='dense').astype(int)
      num_of_ranks = 5
      df_yearly_ret_top = df_yearly_ret[df_yearly_ret['Year % Return Rank'] <= num_of_ranks].copy()
      df_yearly_ret_top = df_yearly_ret_top [['Ticker', 'Year', 'Year % Return', 'Year % Return Rank']]
      df_yearly_ret_top.sort_values(by=['Year', 'Year % Return Rank'], inplace=True)

      print(df_yearly_ret_top.to_string(index=False))

![SP500_Equity_Top_5_Returns_by_Year_Data_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Equity_Top_5_Returns_by_Year_Data_Python.jpg?raw=true)

Let's call our custom function *plot_top_returns_bar_chart* to plot our top 5 performers by year using the *df_yearly_ret_top* dataframe.

      plot_top_returns_bar_chart(df_yearly_ret_top, 'Year')

![SP500_Equity_Top_5_Returns_by_Year_Bar_Charts.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Equity_Top_5_Returns_by_Year_Bar_Charts.jpg?raw=true)

Let's examine the top 10 performers for cumulative returns for the past 4 years. We retrieve the *df_ret_last* dataframe using the last row of our *df_ret* dataframe. We want to ensure that the Tickers span the past 4 years so we find the 1st date that is common among all Tickers and derive the dataframe *df_ret_last_common* where the 1st date is common. We then create a new column using the *rank* function to rank cumulative returns in non-ascending order and cast as an integer. We’ll create a new dataframe called *df_ret_last_top* from slicing *df_ret_last* by *'Cumulative % Return Rank' <= num_of_ranks* where *num_of_ranks = 10*. We then sort *df_ret_last_top* and print the results.

    df_ret = calculate_return(df_pricing.copy(), 'Daily')
    df_ret_last = df_ret.copy().groupby('Ticker').tail(1)
    first_dates = df_ret.groupby('Ticker')['Date'].min().reset_index()
    first_dates.rename(columns={'Date': 'First Date'}, inplace=True)
    df_ret_last = df_ret_last.merge(first_dates, on='Ticker')
    common_first_date = df_ret_last['First Date'].mode()[0]
    df_ret_last_common = df_ret_last[df_ret_last['First Date'] == common_first_date].copy()
    df_ret_last_common.loc[:, 'Cumulative % Return Rank'] = df_ret_last_common.groupby('Date')['Cumulative % Return'].rank(ascending=False, method='dense').astype(int)
    num_of_ranks = 10
    df_ret_last_top = df_ret_last_common[df_ret_last_common['Cumulative % Return Rank'] <= num_of_ranks].copy()
    df_ret_last_top = df_ret_last_top[['Ticker', 'Date', 'Cumulative % Return', 'Cumulative % Return Rank']]
    df_ret_last_top.sort_values(by=['Cumulative % Return Rank'], inplace=True)
    
    print(df_ret_last_top.to_string(index=False))

![SP500_Equity_Top_10_Cumulative_Returns_Data_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Equity_Top_10_Cumulative_Returns_Data_Python.jpg?raw=true)

The results are the same for the same Tickers when using SQL queries except that we filtered out the Tickers that did not exist 4 years back and so **'CEG'**, which was 3rd in the SQL results, was not in this result. **'MPC'** ended up appearing in the list as 10th.

Let's extract the top 10 tickers from our *df_ret* dataframe as *df_ret_top* and compare them in a line chart calling our custom function *plot_returns_line_chart*.

    top_tickers = df_ret_last_top['Ticker'].unique()
    df_ret_top = df_ret[df_ret['Ticker'].isin(top_tickers)].copy()
    plot_returns_line_chart(df_ret_top, 'Daily', 'Cumulative % Return')

![SP500_Equity_Top_10_Cumulative_Returns_Line_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Equity_Top_10_Cumulative_Returns_Line_Chart.jpg?raw=true)

We see that the green line that represents **SMCI** has the highest cumulative return in the last day but has taken a massive drawdown as of February 2024.

Now let's examine the Top 10 Annualized returns using similar ranking logic.

    df_ret_last_common.loc[:, 'Annualized % Return Rank'] = df_ret_last_common.groupby('Date')['Annualized % Return'].rank(ascending=False, method='dense').astype(int)
    num_of_ranks = 10
    df_ret_last_top = df_ret_last_common[df_ret_last_common['Annualized % Return Rank'] <= num_of_ranks].copy()
    df_ret_last_top = df_ret_last_top[['Ticker', 'Date', 'Annualized % Return', 'Annualized % Return Rank']]
    df_ret_last_top.sort_values(by=['Annualized % Return Rank'], inplace=True)

    print(df_ret_last_top.to_string(index=False))

![SP500_Equity_Top_10_Annualized_Returns_Data_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Equity_Top_10_Annualized_Returns_Data_Python.jpg?raw=true)

This gives us the same top performers with what was expected to be earned on average on a yearly basis.

Let's now look at drawdowns compared to the cumulative returns for the top 10 Tickers. A good idea is to exclude the beginning periods where the cumulative return is not yet substantial enough and any change may produce a large value for drawdowns. Let’s use the data as of 3 years ago instead to show the drawdowns. We will simply filter the dates after and including last 3 years and use the custom function *calculate_drawdowns* to return a dataframe called *df_ret_last_top*. We fetch the last record by ticker and sort the Cumulative % Returns in descending order and print the results.

     last_dates = df_quarterly_ret['Date'].max()
     three_years_ago = last_dates - pd.DateOffset(days=365 * 3)
     three_years_ago_str = three_years_ago.strftime('%Y-%m-%d')

     date_filter = (df_ret_top['Date'] >= three_years_ago_str)
     df_ret_top = df_ret_top.loc[date_filter]
     df_ret_top = calculate_drawdowns(df_ret_top, 'Daily')
     df_ret_last_top = df_ret_top.copy().groupby('Ticker').tail(1)
     df_ret_last_top = df_ret_last_top[['Ticker', 'Date', 'Cumulative % Return', 'Annualized % Return', '% Drawdown', 'Max % Drawdown', 'Max Drawdown Date']]
     df_ret_last_top.sort_values(by=['Cumulative % Return'], ascending=False, inplace=True)

     print(df_ret_last_top.to_string(index=False))

![SP500_Equity_Top_10_Cumulative_Returns_Drawdowns_Data_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Equity_Top_10_Cumulative_Returns_Drawdowns_Data_Python.jpg?raw=true)

We can observe that for **SMCI**, the most recent drawdown is **63.20%** represented by *'% Drawdown'* had a **69.33%** maximum drawdown in **2022-04-12**. **VST** had the 2nd highest maximum drawdown and yet the cumulative return was almost 3 times less than **SMCI**. All the top 10 performers had the biggest drawdowns in 2022.

Now let's examine the Top 10 most volatile stocks using Annualized Volatility and ranking logic.

     df_ret_last_common.loc[:, 'Annualized Volatility Rank'] = df_ret_last_common.groupby('Date')['Annualized Volatility'].rank(ascending=False, method='dense').astype(int)
     num_of_ranks = 10
     df_ret_last_top = df_ret_last_common[df_ret_last_common['Annualized Volatility Rank'] <= num_of_ranks].copy()
     df_ret_last_top = df_ret_last_top[['Ticker', 'Date', 'Annualized Volatility', 'Annualized Volatility Rank']]
     df_ret_last_top.sort_values(by=['Annualized Volatility Rank'], inplace=True)

     print(df_ret_last_top.to_string(index=False))

![SP500_Equity_Top_10_Annualized_Volatility_Data_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Equity_Top_10_Annualized_Volatility_Data_Python.jpg?raw=true)

**SMCI** came out as the most volatile stock which can be observed also in the drawdown data and cumulative returns line chart. None of the other top 10 performing stocks were in the top 10 most volatile.

A well known **Risk vs. Reward** measure is the Sharpe Ratio. For more information on this, refer to this link: [Sharpe Ratio: Definition, Formula, and Examples](https://www.investopedia.com/terms/s/sharperatio.asp). It is best to use the **Annualized Sharpe Ratio** which uses annualized returns instead of average returns as it provides a clearer and more reliable measure of risk-adjusted performance. Average returns can be misleading and do not fully capture the dynamics of investment performance over time. The formula can be defined as **(Annualized Return − Risk-Free Rate) / Annulaized Volatility**. Another measure of Risk vs. Reward is the Sortino Ratio. Unlike the Sharpe Ratio, which penalizes both upside and downside volatility, the Sortino Ratio only considers the standard deviation of negative returns, making it more appropriate for assessing investments that may experience high volatility but also provide significant upside potential. For more information, please refer to this link: [Sortino Ratio: Definition, Formula, Calculation, and Example](https://www.investopedia.com/terms/s/sortinoratio.asp). We will also use the **Annualized Sortino Ratio** which is defined as **(Annualized Return − Risk-Free Rate) / Annualized Downside Volatility**. 

Let's first calculate the Annualized Sharpe Ratio and the Annulaized Sortino Ratio. We will first find the top 10 risk-adjusted performers based on Sharpe Ratio. The Risk-Free Rate is based on the 3 month T-Bill rate. We would have to retrieve the daily data for past 4 years to produce a more accurate calculation but we can simply use an average as a rough estimate which is 2.5%.

    df_ret = calculate_return(df_pricing.copy(), 'Daily')
    risk_free_rate = 2.5
    df_ret['Annualized Sharpe Ratio'] = np.where(
        df_ret['Annualized Volatility'] == 0, 
        0, 
        round((df_ret['Annualized % Return'] - risk_free_rate) / df_ret['Annualized Volatility'], 2)
    )
    df_ret['Annualized Sortino Ratio'] = np.where(
        df_ret['Annualized Volatility'] == 0, 
        0, 
        round((df_ret['Annualized % Return'] - risk_free_rate) / df_ret['Annualized Downside Volatility'], 2)
    )
    df_ret_last = df_ret.copy().groupby('Ticker').tail(1)
    first_dates = df_ret.groupby('Ticker')['Date'].min().reset_index()
    first_dates.rename(columns={'Date': 'First Date'}, inplace=True)
    df_ret_last = df_ret_last.merge(first_dates, on='Ticker')
    common_first_date = df_ret_last['First Date'].mode()[0]
    df_ret_last_common = df_ret_last[df_ret_last['First Date'] == common_first_date].copy()
                                             
    df_ret_last_common.loc[:, 'Annualized Sharpe Ratio Rank'] = df_ret_last_common.groupby('Date')['Annualized Sharpe Ratio'].rank(ascending=False, method='dense').astype(int)
    num_of_ranks = 10
    df_ret_last_top = df_ret_last_common[df_ret_last_common['Annualized Sharpe Ratio Rank'] <= num_of_ranks].copy()
    df_ret_last_top = df_ret_last_top[['Ticker', 'Date', 'Annualized Sharpe Ratio', 'Annualized Sharpe Ratio Rank']]
    df_ret_last_top.sort_values(by=['Annualized Sharpe Ratio Rank'], inplace=True)

    print(df_ret_last_top.to_string(index=False))

![SP500_Equity_Top_10_Annualized_Sharpe_Ratio_Data_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Equity_Top_10_Annualized_Sharpe_Ratio_Data_Python.jpg?raw=true)

**LLY** had the top **Annualized Sharpe Ratio** of **1.87** and anything above 1.5 is considered pretty good.

Next, let's look at the top 10 risk-adjusted performers based on Sortino Ratio.

![SP500_Equity_Top_10_Annualized_Sortino_Ratio_Data_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Equity_Top_10_Annualized_Sortino_Ratio_Data_Python.jpg?raw=true)

Most of the same Tickers appear in this list and **LLY** had the top **Annualized Sortino Ratio** of **3.1** and anything above 2.0 is considered excellent.

Another measure of risk vs. reward is the **Calmar Ratio**. For more information on the Calmar Ratio, refer to this link: [What Is the Calmar Ratio, Its Strenths & Weaknesses?](https://www.investopedia.com/terms/c/calmarratio.asp). It is derived by **Annualized Returns / Max Drawdowns** for the past 36 months which is 3 years. Let's filter the returns for the past 3 years, retrieve all the Tickers that were common for past 4 years and calculate the Calmar Ratio by Ticker. We'll then calculate the top 10 risk-adjusted performers based on Calmar Ratio and print the results.  

     last_dates = df_ret['Date'].max()
     three_years_ago = last_dates - pd.DateOffset(days=365 * 3)
     three_years_ago_str = three_years_ago.strftime('%Y-%m-%d')

     date_filter = (df_ret['Date'] >= three_years_ago_str)
     df_ret_filter = df_ret.loc[date_filter].copy()  # Adding .copy() here to avoid the warning
     df_ret_filter = calculate_drawdowns(df_ret_filter)
     df_ret_filter_last = df_ret_filter.groupby('Ticker').tail(1).copy()  # Use .copy() here
     first_dates = df_ret.groupby('Ticker')['Date'].min().reset_index()
     first_dates.rename(columns={'Date': 'First Date'}, inplace=True)
     df_ret_filter_last = df_ret_filter_last.merge(first_dates, on='Ticker')
     common_first_date = df_ret_filter_last['First Date'].mode()[0]
     df_ret_last_common = df_ret_filter_last[df_ret_filter_last['First Date'] == common_first_date].copy() 
     df_ret_last_common['Calmar Ratio'] = np.where(
         df_ret_last_common['Max % Drawdown'] == 0, 
         0, 
         round(df_ret_last_common['Annualized % Return'] / df_ret_last_common['Max % Drawdown'], 2)
     )

     df_ret_last_common.loc[:, 'Calmar Ratio Rank'] = df_ret_last_common.groupby('Date')['Calmar Ratio'].rank(ascending=False, method='dense').astype(int)
     num_of_ranks = 10
     df_ret_last_top = df_ret_last_common[df_ret_last_common['Calmar Ratio Rank'] <= num_of_ranks].copy()
     df_ret_last_top = df_ret_last_top[['Ticker', 'Date', 'Calmar Ratio', 'Calmar Ratio Rank']]
     df_ret_last_top.sort_values(by=['Calmar Ratio Rank'], inplace=True)

     print(df_ret_last_top.to_string(index=False))
           
![SP500_Equity_Top_10_Annualized_Calmar_Ratio_Data_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Equity_Top_10_Annualized_Calmar_Ratio_Data_Python.jpg?raw=true)

Again, **LLY** came in at the top with a **Calmar Ratio** of **1.57** and anything above 1.5.0 is considered strong performance.




