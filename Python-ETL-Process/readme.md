# ETL Process Description

## Python packages needed for the project

For this project, we will be running Python 3.9 in a conda environment. For more information on getting started with conda, please refer to this link: [Getting started with conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html). 

The following packages will need be installed if they do not already exist using conda or pip with the following commands:

conda datetime

conda install sqlalchemy

conda numpy

conda install pandas

conda install urllib

## Create custom re-usable functions: custom_python_functions.py

In all SQL operations, we will need to create a connection to the database. We will also need to clear staging tables before loading. To reuse the code, we can create a Python folder called *Custom_Python_Functions* with a Python file called *custom_python_functions.py* that has all our functions in it. 

*create_connection function* will pass a server name, database name, uid (user id) and passwd (password) and use the SQL Server Native driver to create a connection to the database using the SLQAlchemy package engine. The session factory is bound to the engine and both the session and engine are returned. If no username is provided, the server is assumed to have a trusted connection which is usually the localhost.

import sqlalchemy as sa
import urllib.parse as url

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
        s = sa.orm.sessionmaker(bind=e)
    
        # Return the sessionmaker class and the engine
        return s, e

*clear_table* will pass a session instance and database table name. The table is cleared using a TRUNCATE DDL SQL statement and committing the transaction through our session.

        def clear_table(s1, t):
    
        """
        Clears all rows from the specified database table using a TRUNCATE command.

        Args:
            s1 (Session): The SQLAlchemy session object used to execute the command.
        """
    
        sql_stat = sa.text('TRUNCATE TABLE ' + t)
        s1.execute(sql_stat)
        s1.commit()  # Commit the transaction to make the changes permanent


## Staging the Sector data

We will now import the packages we need and create a database connection by calling our custom function *create_connection*, that can be found in our *Custom_Python_Functions* folder. We use our local server name and our database name to connect and then create a session instance s1 we will use in our code. We then declare our *Data_STG* table and call our clear_table function to clear the table.

        import datetime as dt
        import sqlalchemy as sa
        import os
        import sys
        import urllib.parse as url
        import pandas as pd

        # Setup connection parameters
        comp = os.environ["COMPUTERNAME"]  # Get the computer name from environment variables
        dbase = "Financial_Securities"     # Define the name of the database

        username = os.getlogin()
        external_folder_path = 'C:/Users/' + username + '/Documents/Projects/Financial_Securities/Custom_Python_Functions'
        sys.path.append(external_folder_path)
        from custom_python_functions import create_connection, clear_table


        # Create a connection to the database
        s, e = create_connection(comp, dbase, "", "")
        s1 = s()  # Instantiate a session object

        Base = sa.orm.declarative_base()

        class Data_STG(Base):
    
            """
            SQLAlchemy ORM class representing the 'Data_STG' table in the 'Equities' schema.

            Attributes:
                __tablename__ (str): The name of the table in the database.
                __table_args__ (dict): Additional arguments for the table, including schema name.
                Date (Column): The date column, part of the composite primary key.
                Integer (Column): An integer column.
                Description (Column): A description column, part of the composite primary key.
            """
    
            __tablename__ = 'Data_STG'
            __table_args__ = {'schema': 'Equities'}
            Date = sa.Column(sa.Date, primary_key=True)
            Int_Value1 = sa.Column(sa.Integer, primary_key=True)
            Description = sa.Column(sa.String)

        # Clear the existing data in the Data_STG table
        clear_table(s1, 'Financial_Securities.Equities.Data_STG')

















