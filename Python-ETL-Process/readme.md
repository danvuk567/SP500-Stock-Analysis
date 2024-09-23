# Python ETL Process Description

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


## Staging the Sector data: Load_Sectors_STG.ipynb

We will now import the packages we need and create a database connection by calling our custom function *create_connection*, that can be found in our *Custom_Python_Functions* folder. We can define the path to this folder using our Windows username and sys package. We use our local server name and our database name to connect and then create a session instance s1 we will use in our code. We then declare our *Data_STG* table and call our clear_table function to clear the table.

        import datetime as dt
        import sqlalchemy as sa
        import os
        import sys
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

We define the path to our *GICS_Industries.csv* file, use the current date nad read the file into the pandas dataframe df_sectors and keep only the unique Sector_ID and Sector.
We check if the file exists and loop through the rows and use cnt_recs to keep track of how many rows were loaded. We use an SQL exception that will capture any error but we don't need to raise since we can rerun and clear the table each time we run the commands. After the loop, we issue a commit to our session and then query *Data_STG* to check if the number of records match the number or rows in the dataframe.

        in_file = 'C:/Users/' + username + '/Documents/Projects/Financial_Securities/Data_Files/GICS_Industries.csv' # Path to the CSV file

        curr_date = dt.datetime.now()  # Current date and time

        if os.path.isfile(in_file):
            # Load the CSV file into a DataFrame
            df_sectors = pd.read_csv(in_file)
    

            # Select relevant columns
            df_sectors = df_sectors[['Sector_ID', 'Sector']].drop_duplicates()
    
            # Iterate through the rows of the DataFrame
            for index, row in df_sectors.iterrows():
                try:
                    # Create a new Data_STG instance for each row
                    q1 = Data_STG(
                        Date=curr_date,
                        Int_Value1=row['Sector_ID'],
                        Description=row['Sector']
                    )
                    s1.add(q1)  # Add the instance to the session
            
                # Handle SQLAlchemy errors if they occur during adding the object
                except sa.exc.SQLAlchemyError as e:
                    # Print the error
                    message = f"Issue with updating Data_STG database table for Date: {curr_date} and Sector: {row['Sector']}. Error: {e}"
                    print(message)
    
            # Commit all changes to the database
            s1.commit()

            # SQL query to count the number of records in the Sectors table
            sql_stat = """SELECT COUNT(*) FROM [Financial_Securities].[Equities].[Data_STG]"""

            try: 
                result = e.execute(sql_stat)  # Execute the count query
                cnt_recs = result.scalar()  # Get the count of records
    
            # Handle SQLAlchemy errors if they occur during query execution
            except sa.exc.SQLAlchemyError as e:
            # Print the error
            print(f"Issue querying Data_STG database table for count! Error: {e}")

            # Compare the record counts and print the result    
            if cnt_recs < len(df_sectors):
                print(f"Only {cnt_recs} records out of {len(df_sectors)} records were loaded into the Data_STG table!")
            else:
                print(f"All {cnt_recs} records were loaded into the Data_STG table!")
        else:
            print("File not found!")  # Print a message if the file does not exist

Lastly, we terminate the session s1 to avoid any increased memory usage and ensure that any uncommitted changes are finalized or rolled back.

        s1.close()  # Close the session



## Load the Sectors data: : Load_Sectors.ipynb

We establish a database connection and then query the *Data_STG* table and bind it to the df_sectors dataframe. We will define the *Sectors* table and then loop through the dataframe and query the table to see if the record already exists. We do this in case we want to rerun the code and update the table and if the record does not exist, we do an insert for the columns in *Sectors* referencing the columns in *Data_STG*. If any issues occur, we print the error message, close the session and raise the exception which will halt any further execution. We want to ensure all records are loaded. We do a final check to ensure the number of records match between the *Data_STG* table and the *Sectors* table and close the session.

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

        # SQL query to select values and trim description field from the Data_STG table
        sql_stat = """SELECT 
                       Int_Value1, 
                       TRIM(Description) AS Description
                      FROM [Financial_Securities].[Equities].[Data_STG]
                      ORDER BY Int_Value1"""

        try:              
            df_sectors = pd.read_sql(sql_stat, s1.bind)   # Execute the SQL query through the session and bind the data to the df_sectors dataframe

        # Handle SQLAlchemy errors if they occur during query execution
        except sa.exc.SQLAlchemyError as e:
                # Print the error
                print(f"Issue querying Data_STG database table for count! Error: {e}")
                s1.close()  # Close the session
                raise  # Re-raise the exception to propagate the error

        Base = sa.orm.declarative_base()

        class Sectors(Base):
    
            """
            SQLAlchemy ORM class representing the 'Sectors' table in the 'Equities' schema.

            Attributes:
            __tablename__ (str): The name of the table in the database.
            __table_args__ (dict): Additional arguments for the table, including schema name.
            Sector_ID (Column): A unique identifier for each sector; primary key.
            Name (Column): The name of the sector.
            """
    
            __tablename__ = 'Sectors'
            __table_args__ = {'schema': 'Equities'}
            Sector_ID = sa.Column(sa.Integer, primary_key=True, autoincrement=False)
            Name = sa.Column(sa.String)

            for index, row in df_sectors.iterrows():
            try:
        
                # Query the 'Sectors' table to find records where the 'Sector_ID' column matches the value in the DataFrame's 'Int_Value1' column
                q1 = s1.query(Sectors).filter(Sectors.Sector_ID == row.Int_Value1)

                # Check if any records were found with the specified 'Sector_ID'
                if (q1.count() >= 1):
                    # If one or more records are found, get the first matching record
                    q1 = s1.query(Sectors).filter(Sectors.Sector_ID == row.Int_Value1).first()
                    # Update the 'Name' attribute of the found record with the value from the DataFrame's 'Description' column
                    q1.Name = row['Description']
            
                else:

                    # Create a new Sectors object for each row in df_sectors dataframe
                    q1 = Sectors(
                        Sector_ID=row['Int_Value1'],
                        Name=row['Description']
                    )
                    s1.add(q1)  # Add the instance to the session
        
            except sa.exc.SQLAlchemyError as e:
                # Handle SQLAlchemy errors if they occur during adding the object
                message = f"Issue with updating Sector database table for Name: {row.Description}. Error: {e}"
                print(message)
                s1.close()  # Close the session
                raise  # Re-raise the exception to propagate the error


        s1.commit()  # Commit the transactions to the database

        # SQL query to count the number of records in the Sectors table
        sql_stat3 = """SELECT COUNT(*) FROM [Financial_Securities].[Equities].[Sectors]"""
              
        try: 
            result1 = e.execute(sql_stat3)  # Execute the count query
            cnt_recs2 = result1.scalar()  # Get the count of records
    
        except sa.exc.SQLAlchemyError as e:
            # Handle SQLAlchemy errors if they occur during query execution
            print(f"Issue querying Sectors database table for count! Error: {e}")

        # Compare the record counts and print the result
        if cnt_recs2 < cnt_recs1:
            print(f"Only {cnt_recs2} of {cnt_recs1} records were loaded into Sectors database table!")
        else:
            print(f"All {cnt_recs2} records were loaded into Sectors database table!")         

        s1.close()  # Close the session   


















