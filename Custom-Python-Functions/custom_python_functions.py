# -*- coding: utf-8 -*-
"""
@author: Daniel Vukota
"""

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import urllib.parse as url
import datetime as dt
import pandas as pd
import numpy as np
import plotly as pltly
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
pio.renderers.default='notebook_connected'
import matplotlib.pyplot as plt
import seaborn as sns
import math
from scipy.stats import norm, gaussian_kde
from sklearn.linear_model import LinearRegression


def create_connection(serv, dbase, uid, passwd):
    """
    Creates a connection to a SQL Server database using SQLAlchemy and returns a session and engine.

    Args:
        serv (str): The name or IP address of the SQL Server.
        dbase (str): The name of the database to connect to.
        uid (str): The username for database authentication (leave empty for trusted connection).
        passwd (str): The password for database authentication (needed if uid is provided).

    Returns:
        tuple: A tuple containing the sessionmaker class and the SQLAlchemy engine.
    """
    
    # Check if username is provided; if not, use trusted connection
    if uid == "":
        params = url.quote("DRIVER={SQL Server Native Client 11.0};"
                           "SERVER=" + serv + ";"
                           "DATABASE=" + dbase + ";"
                           "Trusted_Connection=yes")
    else:
        # Create connection parameters for SQL Server using provided username and password
        params = url.quote("DRIVER={SQL Server Native Client 11.0};"
                           "SERVER=" + serv + ";"
                           "DATABASE=" + dbase + ";"
                           "UID=" + uid + ";"  # Username
                           "PWD=" + passwd + ";")  # Password
    
    # Create an SQLAlchemy engine instance with the connection parameters
    e = sa.create_engine("mssql+pyodbc:///?odbc_connect={}".format(params))
    
    # Create a sessionmaker class bound to the engine for managing sessions
    s = sessionmaker(bind=e)
    
    # Return the sessionmaker class and the engine
    return s, e


def clear_table(s1, t):
    
    """
    Clears all rows from the specified database table using a TRUNCATE command.

    Args:
        s1 (Session): The SQLAlchemy session object used to execute the command.
    """
    
    sql_stat = sa.text('TRUNCATE TABLE ' + t)
    s1.execute(sql_stat)
    s1.commit()  # Commit the transaction to make the changes permanent
    
 
def get_dates_for_years(yrs_back, yrs_forward):
    
    """
    Generates the start and end dates for data retrieval.

    Args:
        yrs_back (int): Number of years to look back from the current year.
        yrs_forward (int): Number of years to look forward from the current year.

    Returns:
        tuple: A tuple containing the start date and end date in string format.
    """
 
    if yrs_forward > 0:
            # Calculate the end date as last day of yrs_forward from now
            end_year = int(dt.datetime.now().strftime("%Y")) + yrs_forward
            end_date = str(end_year) + "-12-31"
    else:     
        # Calculate the end date as one day before today
        end_date = (dt.datetime.now() + dt.timedelta(days=-1)).strftime("%Y-%m-%d")
        
    # Calculate the start year by subtracting the given number of years from the current year
    start_year = int(dt.datetime.now().strftime("%Y")) - yrs_back
    # Set the start date to January 1st of the start year
    start_date = str(start_year) + "-01-01"
    
    return start_date, end_date


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
    
    
def calculate_return(df_tmp, period):
    
    """
    Calculate the return percentage based on the 'Close' and 'Open' prices for a given period type.
    
    Parameters:
    - df_tmp: The DataFrame containing the historical data.
    - period: A string indicating the period ('Year', 'Quarter', 'Month', or 'Daily').

    Returns:
    - A DataFrame with new columns: '% Return','Cumulative % Return','Annualized % Return','Annualized Volatility', 
    - 'Annualized Downside Volatility', or None if not applicable.
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
    df_tmp['Prev Close'] = df_tmp.groupby('Ticker')['Close'].shift(1)
    
    # Create a condition for the first period where Prev_Close is NaN
    is_first_period = df_tmp['Prev Close'].isna()
    
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

    # Calculate the rolling Annualized % Return based on Cumulative Simple Return and using no_of_periods and Rolling Return Count
    df_tmp['Annualized % Return'] = ((1 + df_tmp['Cumulative Simple % Return'])**(no_of_periods / df_tmp['Rolling Return Count']) - 1.0)
    
    # Calculate the rolling Annualized Volatility based on Simple Return and using no_of_periods
    df_tmp['Annualized Volatility'] = (df_tmp.groupby('Ticker')['% Return'].expanding(min_periods=1).apply(lambda x: x.std() * np.sqrt(no_of_periods)).reset_index(level=0, drop=True))
    
    # Calculate the rolling Downside Annualized Volatility based on Negative Simple Return and using no_of_periods
    df_tmp['Annualized Downside Volatility'] = (df_tmp.groupby('Ticker')['% Return'].expanding(min_periods=1).apply(lambda x: x[x < 0].std() * np.sqrt(no_of_periods) if not x[x < 0].empty else 0).reset_index(level=0, drop=True))
       
    # Drop the 'Prev_Close', 'Log Return', 'Cumulative Log Return', 'Cumulative Simple % Return' and 'Rolling Return Count' 
    # columns after calculation
    df_tmp.drop(columns=['Prev Close', 'Log Return', 'Cumulative Log Return', 'Cumulative Simple % Return', 'Rolling Return Count'], inplace=True)
    
    # Convert Returns to percentages
    df_tmp['% Return'] = round(df_tmp['% Return'] * 100, 2)
    df_tmp['Cumulative % Return'] = round(df_tmp['Cumulative % Return'] * 100, 2)
    df_tmp['Annualized % Return'] = round(df_tmp['Annualized % Return'] * 100, 2)
    df_tmp['Annualized Volatility'] = round(df_tmp['Annualized Volatility'] * 100, 2)
    df_tmp['Annualized Downside Volatility'] = round(df_tmp['Annualized Downside Volatility'] * 100, 2)
    
    # Drop the 'Prev_Close', 'Log Return', 'Cumulative Log Return', 'Cumulative Simple % Return' and 'Rolling Return Count' 
    # columns after calculation
    df_tmp.drop(columns=['Prev Close', 'Log Return', 'Cumulative Log Return', 'Cumulative Simple % Return', 'Rolling Return Count'], inplace=True)
    
    # Rename the Return column based on period type
    if period != 'Daily':
        df_tmp.rename(columns={'% Return': period + ' % Return'}, inplace=True)    
        df_tmp.rename(columns={'Cumulative % Return': period + ' Cumulative % Return'}, inplace=True)
        df_tmp.rename(columns={'Annualized % Return': period + ' Annualized % Return'}, inplace=True)
        df_tmp.rename(columns={'Annualized Volatility': period + ' Annualized Volatility'}, inplace=True)
        df_tmp.rename(columns={'Annualized Downside Volatility': period + ' Annualized Downside Volatility'}, inplace=True)
        
    return df_tmp

        
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
    df_tmp['Peak'] = df_tmp.groupby('Ticker')[label + 'Cumulative % Return'].cummax()
    
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

def calculate_portfolio_return(df_tmp, period):
    
    """
    Calculate the returns of a portfolio of Tickers using an average of log returns.
    
    Parameters:
    - df_tmp: The DataFrame containing the historical data.
    - period: A string indicating the period ('Year', 'Quarter', 'Month', or 'Daily').

    Returns:
    - A DataFrame with new columns: '% Return', 'Cumulative % Return', 'Annualized % Return', 'Annualized Volatility', 
      'Annualized Downside Volatility', or None if not applicable.
    """
    
    # Assign the number of periods based on the specified period type
    if period == 'Year':
        no_of_periods = 1  # 1 year
    elif period == 'Quarter':
        no_of_periods = 4  # 4 quarters in a year
    elif period == 'Month':
        no_of_periods = 12  # 12 months in a year
    else:
        no_of_periods = 252  # Default to daily data (252 trading days in a year)
        
    if period == 'Daily':
        label = ''
    else:
        label = period + ' '

    # Drop unnecessary columns from the DataFrame to simplify calculations
    df_tmp.drop(columns=['Ticker', 'Open', 'High', 'Low', 'Close', 'Volume', label + 'Annualized % Return', label + 'Annualized Volatility', label + 'Annualized Downside Volatility'], inplace=True)

    # Calculate log returns based on cumulative percentage returns
    df_tmp['Log Return'] = np.log(1 + (df_tmp[label + 'Cumulative % Return'] / 100))

    # Calculate the average log return for each date
    df_tmp['Avg Log Return'] = df_tmp.groupby('Date')['Log Return'].transform('mean')

    # Calculate the average percentage return for each date and convert to decimal
    df_tmp['Avg % Return'] = df_tmp.groupby('Date')[label + '% Return'].transform('mean') / 100

    # Drop columns that are no longer needed after calculating averages
    df_tmp.drop(columns=['Log Return', label + '% Return', label + 'Cumulative % Return'], inplace=True)

    # Calculate cumulative percentage return from average log return
    df_tmp['Cumulative % Return'] = np.exp(df_tmp['Avg Log Return']) - 1

    # Drop the average log return column as it is no longer needed
    df_tmp.drop(columns=['Avg Log Return'], inplace=True)

    # Rename the average percentage return column to '% Return' for clarity
    df_tmp.rename(columns={'Avg % Return': '% Return'}, inplace=True)

    # Remove duplicate entries in the DataFrame
    df_tmp.drop_duplicates(inplace=True)

    # Count the number of returns in a rolling manner, starting from the first entry
    df_tmp['Rolling Return Count'] = df_tmp['% Return'].expanding(min_periods=1).count()
    
    # Calculate annualized return based on cumulative return and the number of returns
    df_tmp['Annualized % Return'] = ((1 + df_tmp['Cumulative % Return']) ** (no_of_periods / df_tmp['Rolling Return Count']) - 1)

    # Calculate annualized volatility based on the standard deviation of percentage returns
    df_tmp['Annualized Volatility'] = df_tmp['% Return'].expanding().std() * np.sqrt(no_of_periods)

    # Calculate annualized downside volatility (only for negative returns)
    df_tmp['Annualized Downside Volatility'] = df_tmp['% Return'].expanding().apply(
        lambda x: x[x < 0].std() * np.sqrt(no_of_periods) if len(x[x < 0]) > 0 else 0)

    # Drop the rolling return count column after its use
    df_tmp.drop(columns=['Rolling Return Count'], inplace=True)

    # Round the values for presentation to two decimal places
    df_tmp['% Return'] = round(df_tmp['% Return'] * 100, 2)
    df_tmp['Cumulative % Return'] = round(df_tmp['Cumulative % Return'] * 100, 2)
    df_tmp['Annualized % Return'] = round(df_tmp['Annualized % Return'] * 100, 2)
    df_tmp['Annualized Volatility'] = round(df_tmp['Annualized Volatility'] * 100, 2)
    df_tmp['Annualized Downside Volatility'] = round(df_tmp['Annualized Downside Volatility'] * 100, 2)
    
    # Rename return columns based on the specified period type, if not daily
    if period != 'Daily':
        df_tmp.rename(columns={'% Return': period + ' % Return'}, inplace=True)    
        df_tmp.rename(columns={'Cumulative % Return': period + ' Cumulative % Return'}, inplace=True)
        df_tmp.rename(columns={'Annualized % Return': period + ' Annualized % Return'}, inplace=True)
        df_tmp.rename(columns={'Annualized Volatility': period + ' Annualized Volatility'}, inplace=True)
        df_tmp.rename(columns={'Annualized Downside Volatility': period + ' Annualized Downside Volatility'}, inplace=True)
        
    return df_tmp  # Return the modified DataFrame



def plot_return_histogram(df_tmp, return_type, ticker):
    
    """
    Plot a histogram of '% Return' for a specific ticker with a normal distribution curve based on all tickers.
    
    Parameters:
    - df_tmp: DataFrame containing return data for all tickers.
    - return_type: Name of the column containing percentage returns.
    - ticker: Ticker symbol to filter the DataFrame.
    """
    
    # Filter rows for the specific ticker
    df_ticker = df_tmp[df_tmp['Ticker'] == ticker]
    
    # Ensure the DataFrame contains the required columns
    if return_type not in df_tmp.columns:
        raise ValueError(f"Required column '{return_type}' is missing.")
    
    # Compute global mean and standard deviation from all tickers
    all_returns = df_tmp[return_type]
    global_mean = np.mean(all_returns)
    global_std_dev = np.std(all_returns)
    
    # Compute histogram for the specific ticker
    ticker_returns = df_ticker[return_type]
    
    # Calculate the interquartile range (IQR)
    IQR = np.percentile(ticker_returns, 75) - np.percentile(ticker_returns, 25)
    
    # Calculate the bin width using the Freedman-Diaconis rule
    bin_width = 2 * IQR / np.cbrt(len(ticker_returns))
    
    # Calculate the optimal bin width using Freedman-Diaconis rule
    num_bins = int((ticker_returns.max() - ticker_returns.min()) / bin_width)
    
    plt.figure(figsize=(12, 8))
    
    # Compute histogram and keep counts (not densities)
    count, bins, _ = plt.hist(ticker_returns, bins=num_bins, alpha=0.6, density=False, edgecolor='black', label=f'Frequency for {ticker}')
    total_count = np.sum(count)
    
    # Compute KDE for a smooth line
    kde = gaussian_kde(ticker_returns, bw_method='scott')  # 'scott' method automatically chooses bandwidth
    x_kde = np.linspace(ticker_returns.min(), ticker_returns.max(), 1000)  # Generate points for smooth line
    y_kde = kde(x_kde)  # KDE values
    y_kde_normalized = y_kde * len(ticker_returns) * bin_width  # Normalize KDE to match histogram counts   
    plt.plot(x_kde, y_kde_normalized, 'g-', linewidth=2, label='KDE (Smooth Line) for ' + ticker)
    
    # Calculate bin width for scaling the normal distribution
    actual_bin_width = bins[1] - bins[0]  # Use the actual bin width from the histogram calculation
    
    # Plot the normal distribution curve based on all tickers and scale to match histogram
    x = np.linspace(min(bins), max(bins), 100)
    p = norm.pdf(x, global_mean, global_std_dev)  # PDF of the normal distribution
    p = p * total_count * actual_bin_width  # Scale PDF by total count and bin width to match frequency

    # Plot the normal distribution curve
    plt.plot(x, p, 'r-', linewidth=2, label='Normal Distribution (All Tickers)')
    
    # Add red dotted vertical line at x = 0
    plt.axvline(x=0, color='red', linestyle='--', linewidth=2, label='x = 0')
    
    # Set labels and title
    plt.xlabel(return_type)
    plt.ylabel('Frequency')
    plt.title(f'Frequency Histogram of {return_type} for {ticker} with Normal Distribution Curve')
    
    # Add legend and grid
    plt.legend()
    plt.grid(True)
    plt.show()    

    
def plot_returns_bubble_chart(df_tmp, return_type, size_type):
    
    """
    Plot a bubble chart where the x-axis is Ticker, 
    y-axis is return_type.
    
    Parameters:
    - df: DataFrame with columns 'Ticker', return_type, and other metric as size_type
    """
    
    # Filter out rows where size_type has negative or zero values
    df_tmp2 = df_tmp[df_tmp[size_type] > 0].copy()
   

    # Sort by the size_type and get the top 10 tickers
    top_10_tickers = df_tmp2.nlargest(10, size_type)[['Ticker', return_type, size_type]]
    
    fig = px.scatter(
        df_tmp2, 
        x='Ticker',  # X-axis is Ticker
        y=return_type,  # Y-axis is return_type
        size=size_type,  # Bubble size based on size_type
        color='Ticker',  # Different colors for different tickers
        hover_name='Ticker',  # Display Ticker name on hover
        size_max=60,  # Maximum bubble size
        title=f"Bubble Chart: {return_type} by Ticker with Bubble Size as {size_type}",
    )
    
    # Customize chart appearance
    fig.update_layout(
        xaxis_title="Ticker",
        yaxis_title=return_type,
        showlegend=False,
        plot_bgcolor="lightgrey"  # Set background color
    )
    
    # Add an annotation for the top 10 tickers
    annotations = []
    for i, row in top_10_tickers.iterrows():
        # Get the corresponding y value
        y_value = df_tmp2.loc[df_tmp2['Ticker'] == row['Ticker'], return_type].values[0]
        annotations.append(
            dict(
                x=row['Ticker'],
                y=y_value,
                xref="x",
                yref="y",
                text=row['Ticker'],  # Show Ticker name
                showarrow=True,
                arrowhead=2,
                ax=50,  # Move the annotation right
                ay=-20,  # Adjust the vertical position of annotation
                font=dict(size=10, color="black")
            )
        )

    # Add the annotations to the layout
    fig.update_layout(annotations=annotations)

    # Create a separate legend box on the right for the top 10 tickers
    legend_text = '<br>'.join([f"{row['Ticker']}, {row[size_type]}" for _, row in top_10_tickers.iterrows()])
    
    # Add a text box to display the top 10 tickers legend
    fig.add_annotation(
        dict(
            x=1.05,  # Position the legend outside of the plot
            y=0.5,  # Vertically center the legend
            xref='paper', 
            yref='paper',
            showarrow=False,
            text=f'<b>Top 10 Tickers by<br>{size_type}</b><br>{legend_text}',
            font=dict(size=12, color="black"),
            align='left',
            bordercolor='black',
            borderwidth=1,
            borderpad=5,
            bgcolor="lightgrey"
        )
    )

    # Show the figure
    fig.show()
    
    
    
def plot_period_returns_by_ticker_box_plot(df_ret, period):
    
    """
    Plots a box plot of returns for a given ticker and period.
    
    Parameters:
    - df_ret: DataFrame containing return data.
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
    period_label = '' if period == 'Daily' else f'{period} '

    # Create the boxplot, with 'Ticker' on the x-axis and returns on the y-axis
    sns.boxplot(x='Ticker', y=f'{period_label}% Return', data=df_ret, hue='Ticker', palette="Set2", flierprops=flierprops, legend=False)
    plt.title(f'{period_label}% Returns by Ticker')  
    plt.ylabel(f'{period_label}% Returns')  
    plt.xlabel('Ticker')
                      
    # Add gridlines to the y-axis for clarity, using a dashed line style and slight transparency
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Rotate the x-axis labels by 45 degrees for better readability, especially if there are many years
    plt.xticks(rotation=45)
    
    # Display the plot
    plt.show()
    
    
def plot_ticker_correlations(df_tmp, return_type):
    
    """
    Compute and visualize the correlation between the returns of different tickers.
    
    Parameters:
    - df_tmp: DataFrame containing return data for multiple tickers.
    - return_type: Column name containing the returns to be correlated.

    
    Returns:
    - Correlation matrix and heatmap.
    """
    
    # Pivot the DataFrame to have tickers as columns and dates as index
    df_pivot = df_tmp.pivot_table(index='Date', columns='Ticker', values=return_type)
    
    # Calculate the correlation matrix
    corr_matrix = df_pivot.corr()
    
    # Plot the heatmap of the correlation matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0,
                cbar_kws={'label': 'Correlation'}, linewidths=0.5)
    
    plt.title(f'Correlation between Tickers based on {return_type}')
    plt.show()
    
    return corr_matrix


def scatter_plot(df_tmp, return_type):

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.linear_model import LinearRegression


    # Create a scatter plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Date', y=return_type, data=df_tmp)

    # Fit a linear regression model
    X = np.array(range(len(df_tmp))).reshape(-1, 1)  # Dates as numerical values
    y = df_tmp[return_type].values
    model = LinearRegression()
    model.fit(X, y)
    predicted = model.predict(X)

    # Plot the regression line
    plt.plot(df_tmp['Date'], predicted, color='red', linewidth=2, label='Regression Line')

    # Add labels and title
    plt.title(f'{return_type} with Regression Line')
    plt.xlabel('Date')
    plt.ylabel(f'{return_type}')
    plt.legend()
    plt.show()






    
        
    


    
    
