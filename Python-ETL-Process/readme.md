# ETL Process Description

## Python packages needed for the project

For this project, we will be running Python 3.9 in a conda environment. For more information on getting started with conda, please refer to this link: [Getting started with conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html). 

The following packages will need be installed using conda or pip with the following commands:

conda install sqlalchemy

conda install os

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

















