# -*- coding: utf-8 -*-
"""
@author: Daniel Vukota
"""

import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import urllib.parse as url
import datetime as dt


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


def get_pricing_data(df_pricing, period):
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
    df_tmp = df_tmp.groupby(required_cols).agg(
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
    return df_tmp

  
