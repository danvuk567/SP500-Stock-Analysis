# Python ETL Process Description

## Python packages needed for the project

For this project, we will be running Python 3.9 in a conda environment. For more information on getting started with conda, please refer to this link: [Getting started with conda](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html). 

The following packages will need be installed if they do not already exist using conda or pip with the following commands:

conda install datetime

conda install sqlalchemy

conda install numpy

conda install pandas

conda install urllib

pip install yfinance

conda install time

pip install pandas_market_calendars

pip install plotly

conda install matplotlib

conda install seaborn

conda install scipy

conda install sklearn

pip install cryptography



## Create custom re-usable functions: *[custom_python_functions.py](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Custom_Python_Functions/custom_python_functions.py)*  

In all SQL operations, we will need to create a connection to the database. We will also need to clear staging tables before loading. To reuse the code, we can create a Python folder called *Custom_Python_Functions* with a Python file called *custom_python_functions.py* that has all our functions in it. 

*create_connection function* will pass a server name, database name, uid (user id) and passwd (password) and use the SQL Server Native driver to create a connection to the database using the SLQAlchemy package engine. The session factory is bound to the engine and both the session and engine are returned. If no username is provided, the server is assumed to have a trusted connection which is usually the localhost.

    import sqlalchemy as sa
    import urllib.parse as url

    def create_connection(serv, dbase, uid, passwd):
        """
        Creates a connection to a SQL Server database using SQLAlchemy and returns a session and engine.

        Args:
            serv: String specifying the name or IP address of the SQL server.
            dbase: String specifying the name of the database to connect to.
            uid  String specifying the username for database authentication (leave empty for trusted connection).
            passwd: String specifying the password for database authentication (needed if uid is provided).

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

Usernames and passwords should not be visible in code for security purposes and manually entering them each time they are required can be tedious and not feasible for automated processes. 
We can use encrypted username and passwords with the help of a Python module called *Fernet* within the *cryptography* package. The function *write_key* will generate a key and save it to a key file. 
The *load_key* function will read the key from the key file and the *encrypt* function will use that key to encrypt the data in our target file. We can use the the *write_key*, *load_key* and the *encrypt* functions
to encrypt text files containing usernames and passwords. The *decrypt* function is used to to decrypt the data from the encrypted file using the same key we retrieved from the *load_key* function. This way, we can retrieve the username and password and store them in variables. For more information on how to use Fernet, you can refer to this link: [Fernet (symmetric encryption)](https://cryptography.io/en/latest/fernet/#cryptography.fernet.Fernet.generate_key).

        from cryptography.fernet import Fernet

        def write_key(path, key_file):
    
            """
            Generates a key and saves it into a file.
    
            Parameters:
            path (str): The directory path where the key file will be saved.
            key_file (str): The name of the file (including extension) to save the key.
            """
    
            # Generate a new cryptographic key using Fernet
            key = Fernet.generate_key()
    
            # Open a file in binary write mode to save the key
            with open(path + key_file, "wb") as key_file:
                # Write the generated key to the file
                key_file.write(key)
        
            key_file.close()


        def load_key(path, key_file):
    
            """
            Loads a cryptographic key from a specified file.

            Parameters:
            path (str): The directory path where the key file is located.
            key_file (str): The name of the file (including extension) from which to load the key.

            Returns:
            bytes: The cryptographic key read from the file.
            """
    
            # Open the specified key file in binary read mode and return its contents
            with open(path + key_file, "rb") as key_file:
                return key_file.read()


        def encrypt(path, filename, key):
    
            """
            Encrypts a file using the provided cryptographic key.

            Parameters:
            path (str): The directory path where the file is located.
            filename (str): The name of the file to be encrypted.
            key (bytes): The cryptographic key used for encryption.
            """
    
            # Create a Fernet cipher object using the provided key
            f = Fernet(key)

            # Open the specified file in binary read mode
            with open(path + filename, "rb") as file:
                # Read all file data into memory
                file_data = file.read()

            # Encrypt the file data using the Fernet cipher
            encrypted_data = f.encrypt(file_data)

            # Open the same file in binary write mode to overwrite it with the encrypted data
            with open(path + filename, "wb") as file:
                # Write the encrypted data back to the file
                file.write(encrypted_data)


        def decrypt(path, filename, key):
    
            """
            Decrypts a file using the provided cryptographic key.

            Parameters:
            path (str): The directory path where the file is located.
            filename (str): The name of the file to be decrypted.
            key (bytes): The cryptographic key used for decryption.

            Returns:
            str: The decrypted file data as a UTF-8 string.
            """
    
            # Create a Fernet cipher object using the provided key
            f = Fernet(key)
    
            # Open the specified file in binary read mode
            with open(path + filename, "rb") as file:
                # Read the encrypted data from the file
                encrypted_data = file.read()
    
            # Decrypt the encrypted data using the Fernet cipher
            decrypted_data = f.decrypt(encrypted_data)
    
            # Convert the decrypted bytes to a UTF-8 string and return it
            return str(decrypted_data, 'utf-8')


*clear_table* will pass a session instance and database table name. The table is cleared using a *TRUNCATE* DDL SQL statement and committing the transaction through our session.

        def clear_table(s1, t):
    
        """
        Clears all rows from the specified database table using a TRUNCATE command.

        Args:
        s1: The SQLAlchemy session object used to execute the command.
        t: String representing the table name.
        """
    
        sql_stat = sa.text('TRUNCATE TABLE ' + t)
        s1.execute(sql_stat)
        s1.commit()  # Commit the transaction to make the changes permanent


*get_dates_for_years* will pass the number of years back and number of years forward. It will return the 1st day of the year as the start date for years back. And it will return for the end date as the last day of the year for years forward > 0, otherwise it returns yesterday's date.

            def get_dates_for_years(yrs_back, yrs_forward):
    
            """
            Generates the start and end dates for data retrieval.

            Args:
                yrs_back: Integer specifying the number of years to look back from the current year.
                yrs_forward: Integer specifying the number of years to look forward from the current year.

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


## Stage the Sectors data: *[Load-Sectors_STG.ipynb](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-ETL-Process/Load-Sectors_STG.ipynb)*  

We will now import the packages we need and create a database connection by calling our custom function *create_connection*, that can be found in our *custom_python_functions.py* Python file in our *Custom_Python_Functions* folder. We can define the path to this folder using our Windows username and sys package. To connect to our Microsoft Azure database using this function, we will pass the server name,
the database name along with the username and password. For this project, we have stored our username in the file *user_key.txt* that we encrypted using *Fernet* along with the key file *user_key.ky*. The password is stored in *pass_key.txt* along with the key file *pass_key.ky*. Both files are found in the *Custom_Python_Functions* folder. We use the *load_key* function to retrieve our keys and the *decrypt* function to decrypt and retrieve our username and password using the keys. Both these functions can be found in our  *custom_python_functions.py* Python file in our *Custom_Python_Functions* folder. Once the connection is established, we create a session instance s1 that we will use to interact with the database. We then declare our *Data_STG* table and call our clear_table function to clear the table.

        import datetime as dt
        import sqlalchemy as sa
        import os
        import sys
        import pandas as pd

        username = os.getlogin()
        external_folder_path = 'C:/Users/' + username + '/Documents/Projects/Financial_Securities/Custom_Python_Functions/'
        sys.path.append(external_folder_path)
        from custom_python_functions import create_connection, clear_table, load_key, decrypt

        key1 = 'user_key.ky'
        key_file1 = 'user_key.txt'
        key2 = 'pass_key.ky'
        key_file2 = 'pass_key.txt'

        key1 = load_key(f_path, key1)
        uid = decrypt(f_path, key_file1, key1)

        key2 = load_key(f_path, key2)
        passwd = decrypt(f_path, key_file2, key2) 

        # Setup connection parameters
        server = 'danvuk.database.windows.net'
        dbase = 'Financial_Securities'
        
        # Create a connection to the database
        s, e = create_connection(server, dbase, uid, passwd)
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

We define the path to our *GICS_Industries.csv* file, use the current date and read the file into the pandas dataframe df_sectors and keep only the unique Sector_ID and Sector records.
We check if the file exists and loop through the rows and use *cnt_recs* to keep track of how many rows were loaded. We use an SQL exception that will capture any error that we don't need to raise since we can rerun and clear the table each time we run the commands. After the loop, we issue a commit to our session and then query *Data_STG* to check if the number of records match the number or rows in the dataframe.

        in_file = 'C:/Users/' + username + '/Documents/Projects/Financial_Securities/Data-Source-Files/GICS_Industries.csv' # Path to the CSV file

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

            print("Database data load is complete")

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



## Load the Sectors data: *[Load-Sectors.ipynb](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-ETL-Process/Load-Sectors.ipynb)*  

We establish a database connection and then query the *Data_STG* table and bind it to the df_sectors dataframe. We will define the *Sectors* table and then loop through the dataframe and query the table to see if the record already exists. We do this in case we want to rerun the code and update the table and if the record does not exist, we do an insert for the columns in *Sectors* referencing the columns in *Data_STG*. If any issues occur, we print the error message, close the session and raise the exception which will halt any further execution. We want to ensure all records are loaded. We do a final check to ensure the number of records match between the *Data_STG* table and the *Sectors* table and close the session.

        import sqlalchemy as sa
        import os
        import sys
        import urllib.parse as url
        import pandas as pd

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

            # Handle SQLAlchemy errors if they occur during query execution
            except sa.exc.SQLAlchemyError as e:
                message = f"Issue with updating Sector database table for Name: {row.Description}. Error: {e}"
                print(message)
                s1.close()  # Close the session
                raise  # Re-raise the exception to propagate the error


        s1.commit()  # Commit the transactions to the database

        print("Database data load is complete")

        # SQL query to count the number of records in the Data_STG table
        sql_stat2 = """SELECT COUNT(*) FROM [Financial_Securities].[Equities].[Data_STG]"""
          
        try: 
            result1 = e.execute(sql_stat2)  # Execute the count query
            cnt_recs1 = result1.scalar()  # Get the count of records

        # Handle SQLAlchemy errors if they occur during query execution
        except sa.exc.SQLAlchemyError as e:
            print(f"Issue querying Data_STG database table for count! Error: {e}")

        # SQL query to count the number of records in the Sectors table
        sql_stat3 = """SELECT COUNT(*) FROM [Financial_Securities].[Equities].[Sectors]"""
              
        try: 
            result1 = e.execute(sql_stat3)  # Execute the count query
            cnt_recs2 = result1.scalar()  # Get the count of records

        # Handle SQLAlchemy errors if they occur during query execution
        except sa.exc.SQLAlchemyError as e:
            print(f"Issue querying Sectors database table for count! Error: {e}")

        # Compare the record counts and print the result
        if cnt_recs2 < cnt_recs1:
            print(f"Only {cnt_recs2} of {cnt_recs1} records were loaded into Sectors database table!")
        else:
            print(f"All {cnt_recs2} records were loaded into Sectors database table!")         

        s1.close()  # Close the session   

## Stage Industry Groups data: *[Load-Industry_Groups_STG.ipynb](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-ETL-Process/Load-Industry_Groups_STG.ipynb)* 

This process is similar to staging the Sectors data so I won't go into details. We load the file *GICS_Industries.csv* and in this case, keep the unique Industry_Group_ID, Industry_Group and Sector_ID records.
We then load the data into the *Data_STG* table.

## Load Industry Groups data: *[Load-Industry_Groups.ipynb](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-ETL-Process/Load-Industry_Groups.ipynb)*

This process will load the *Industry_Groups* table with Industry Group data and Sector_ID from the *Data_STG* table.

## Stage Industries data: *[Load-Industries_STG.ipynb](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-ETL-Process/Load-Industries_STG.ipynb)*

We load the file *GICS_Industries.csv* and in this case, keep the unique Industry_ID, Industry and Industry_Group_ID records. We then load the data into the *Data_STG* table.

## Load Industries data: *[Load-Industries.ipynb](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-ETL-Process/Load-Industries.ipynb)*

This process will load the *Industries* table with Industry data and Industry_Group_ID from the *Data_STG* table.

## Stage Sub-Industries data: *[Load-Sub_Industries_STG.ipynb](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-ETL-Process/Load-Sub_Industries_STG.ipynb)*

We load the file *GICS_Industries.csv* and in this case, keep the unique Sub_Industry_ID, Sub_Industry and Industry_ID records. We then load the data into the *Data_STG* table.

## Load Sub-Industries data: *[Load-Sub_Industries.ipynb](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-ETL-Process/Load-Sub_Industries.ipynb)*

This process will load the *Industries* table with Sub_Industry data and Industry_ID from the *Data_STG* table.

## Stage Equities data: *[Load-Equities_STG.ipynb](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-ETL-Process/Load-Equities_STG.ipynb)*

We load the file *SP500_GICS_Combined.csv* that we merged with all Equity data if the tickers match the tickers found in the *SP500_Equities_Prices.csv* file. The last row in the *SP500_Equities_Prices.csv* file is removed as there are usually comments at the end of the data from Barchart. We compare the 2 sources to ensure we have the latest valid list of S&P500 tickers. If the tickers are valid, we keep the Ticker, Name and Sub_Industry_ID records from *SP500_GICS_Combined.csv*. We then load the data into the *Data_STG* table.

## Load Equities data: *[Load-Equities.ipynb](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-ETL-Process/Load-Equities.ipynb)* 

This process will load the *Equities* table with Equity data and Sub_Industry_ID from the *Data_STG* table.

## Stage Yahoo Equity Pricing data: *[Load-Yahoo_Equity_Prices_STG.ipynb](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-ETL-Process/Load-Yahoo_Equity_Prices_STG.ipynb)*

For this process, we'll go into some new types of code. We will import the packages needed and 2 other packages, *yfinance* and *time*. After establishing a connection, we define the staging table *Data_STG* to store the pricing data we will retrieve from **Yahoo Finance**. We then clear the *Data_STG* table.

        import datetime as dt
        import sqlalchemy as sa
        import os
        import sys
        import pandas as pd
        import yfinance as yf
        import time
        
        Base = sa.orm.declarative_base()

        class Data_STG(Base):
    
            """
            SQLAlchemy ORM class representing the 'Data_STG' table in the 'Equities' schema.

            Attributes:
            __tablename__ (str): The name of the table in the database.
            __table_args__ (dict): Additional arguments for the table, including schema name.
            Date (Column): The date column, used as part of the primary key.
            Description (Column): The description column, used as part of the primary key.
            Float_Value1 (Column): A column for storing floating-point values, such as stock prices or metrics.
            Float_Value2 (Column): Another column for storing floating-point values.
            Float_Value3 (Column): Another column for storing floating-point values.
            Float_Value4 (Column): Another column for storing floating-point values.
            Int_Value1 (Column): A column for storing integer values, such as volumes or counts.
            """
    
            __tablename__ = 'Data_STG'
            __table_args__ = {'schema': 'Equities'}
            Date = sa.Column(sa.Date, primary_key=True)
            Description = sa.Column(sa.String, primary_key=True)
            Float_Value1 = sa.Column('Float_Value1', sa.Float)
            Float_Value2 = sa.Column('Float_Value2', sa.Float)
            Float_Value3 = sa.Column('Float_Value3', sa.Float)
            Float_Value4 = sa.Column('Float_Value4', sa.Float)
            Int_Value1 = sa.Column('Int_Value1', sa.BigInteger)  

            # Clear the existing data in the Data_STG table
            clear_table(s1, 'Financial_Securities.Equities.Data_STG')

Next, we'll use the Tickers we have loaded in the Equities table and store them in a dataframe and convert the values to a list called *ticker_list*.

            # Define SQL query to retrieve tickers from the Equities table
            sql_stat = """SELECT
              TRIM(Ticker) AS Ticker
              FROM [Financial_Securities].[Equities].[Equities]
              ORDER BY Ticker"""

            try:
                # Execute the SQL query and read the results into a DataFrame
                df_tickers = pd.read_sql(sql_stat, s1.bind)
                # Store the values as a list
                ticker_list = df_tickers['Ticker'].values.tolist()

                # Handle exceptions during SQL query execution
                except sa.exc.SQLAlchemyError as e:
                print(f"Issue querying Equities database table! Error: {e}")
                s1.close()
                raise

We then call the custom function *get_dates_for_years* function for 3 years back from the current year and 0 years forward to use dates to fetch the last 4 years of pricing data.

            # Generate the date range of 3 years back as of yesterday
            start_date, end_date = get_dates_for_years(3, 0)

Next, we define a function to get the pricing data from Yahoo Finance API for the ticker, start_date and end_date we pass. Closing prices simply refer to the cost of shares at the end of the day, whereas adjusted closing prices take dividends, stock splits, and new stock offerings into account. For more information on this, refer to this link: [Adjusted Closing Price: How It Works, Types, Pros & Cons](https://www.investopedia.com/terms/a/adjusted_closing_price.asp). For our analysis, we only want prices that are influenced by buyers and sellers, so we want to retrieve adjusted prices. To to make sure all prices are adjusted, we retrieve the Open, High, Low and Close prices and divide all the prices by the *Factor = Close / Adj Close*. Some stocks have multiple classes and so those tickers will have a suffix of class A, B or C. For more information on this, refer to this link: [Dual Class Stock: Definition, Structure, and Controversy](https://www.investopedia.com/terms/d/dualclassstock.asp). For those cases, the ticker notation may have a "." or "-" or "/" denoting the suffix. Our multi-class Equity tickers were suffixed using "." and Yahoo Finance uses "-" so we will replace the string for thos cases when calling the API function. Finally, we check if all the tickers were fetched from our ticker list.


        def create_daily_pricing(ticker, start_date, end_date):
    
        """
        Retrieves and processes daily pricing data for a given ticker symbol.

        Args:
            ticker (str): The stock ticker symbol.
            start_date (str): The start date for the data retrieval.
            end_date (str): The end date for the data retrieval.

        Returns:
            a DataFrame with daily pricing data.
        """
    
        # Download stock data from Yahoo Finance
        stock_data = yf.download(ticker.replace(".", "-"), start=start_date, end=end_date)
    
        # Copy the data for processing
        df_tmp = stock_data.copy()
        df_tmp['Ticker'] = ticker
        df_tmp.reset_index(inplace=True)
        df_tmp['Date'] = pd.to_datetime(df_tmp['Date'], format='%Y-%m-%d')
    
        # Fill missing values using forward fill method
        df_tmp['Open'] = df_tmp['Open'].fillna(method="ffill")
        df_tmp['High'] = df_tmp['High'].fillna(method="ffill")
        df_tmp['Low'] = df_tmp['Low'].fillna(method="ffill")
    
        # Adjust prices and calculate the factor for adjustments based on Close vs. Adjusted Close 
        df_tmp['Factor'] = df_tmp['Close'] / df_tmp['Adj Close']
        df_tmp['Close'] = round(df_tmp['Adj Close'].fillna(method="ffill"), 2)
        df_tmp['Factor'] = df_tmp['Close'] / df_tmp['Adj Close']
        df_tmp['Open'] = round(df_tmp['Open'] / df_tmp['Factor'], 2)
        df_tmp['High'] = round(df_tmp['High'] / df_tmp['Factor'], 2)
        df_tmp['Low'] = round(df_tmp['Low'] / df_tmp['Factor'], 2)
    
        # Select relevant columns and prepare DataFrame for database insertion
        df_tmp = df_tmp[['Ticker', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        df_tmp['Date2'] = df_tmp['Date']
        df_tmp.set_index(['Date2'], inplace=True)
        df_tmp.sort_values(by=['Date'], inplace=True)

        return df_tmp

        if len(df_equities['Ticker'].drop_duplicates()) < len(ticker_list):
            print(f"Only {len(df_equities['Ticker'].drop_duplicates())} records out of {len(ticker_list)} records were fetched!")
        else:
            print(f"All {len(ticker_list)} records were fetched!")

We will then loop through our Tickers in our ticker list and store our pricing data using the create_daily_pricing function in the df_equities dataframe. We allow 1 second to pass using the sleep function from the time package before fetching each Ticker data to avoid any API rate limits. This will take some time to run to fetch pricing history for roughly 500 Tickers.

        # Initialize variables for processing
        first_ticker = True

        for ticker in ticker_list:
            # Fetch and process daily pricing data for each ticker
            df_tmp = create_daily_pricing(ticker, start_date, end_date)
    
            if len(df_tmp) > 0:
                # Combine data for all tickers into a single DataFrame
                if first_ticker:
                    df_equities = df_tmp.copy()
                    first_ticker = False
                else:
                    df_equities = pd.concat([df_equities, df_tmp])
        
                # Sleep to avoid hitting API rate limits
                time.sleep(1)

        print("Pricing data fetch is complete")
      
We load the data into Data_STG and raise an exception to halt further processing if there are any issues so that we ensure all the pricing data is loaded.

        # Insert the data into the Data_STG table
        for index, row in df_equities.iterrows():
            try:
                q1 = Data_STG(
                    Date=row['Date'],
                    Description=row['Ticker'],
                    Float_Value1=row['Open'],
                    Float_Value2=row['High'],
                    Float_Value3=row['Low'],
                    Float_Value4=row['Close'],
                    Int_Value1=row['Volume'],
                )
                s1.add(q1)

            # Handle exceptions during data insertion
            except sa.exc.SQLAlchemyError as e:
                message = f"Issue with updating Data_STG database table for Ticker: {row['Ticker']}. Error: {e}"
                print(message)
                s1.close()
                raise

        # Commit all changes to the database
        s1.commit()  

        print("Database data load is complete")

And finally, we check if all records were loaded in the *Data_STG* table and close the session.

    # SQL query to count the number of records in the Data_STG table
    sql_stat = """SELECT COUNT(*) FROM [Financial_Securities].[Equities].[Data_STG]"""

    try: 
        result = e.execute(sql_stat)  # Execute the count query
        cnt_recs = result.scalar()  # Get the count of records
    
    # Handle SQLAlchemy errors if they occur during query execution
    except sa.exc.SQLAlchemyError as e:
        # Print the error
        print(f"Issue querying Data_STG database table for count! Error: {e}")

        
    # Compare the record counts and print the result    
    if cnt_recs < len(df_equities):
        print(f"Only {cnt_recs} records out of {len(df_equities)} records were loaded into the Data_STG table!")
    else:
        print(f"All {cnt_recs} records were loaded into the Data_STG table!")

    s1.close()  # Close the session


## Load Market Calendar data: *[Load-US_Market_Calendar.ipynb](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-ETL-Process/Load-US_Market_Calendar.ipynb)*

To determine if there is missing Equity pricing data for any Ticker for the same range of dates, we need to validate it against US market dates. We can retrieve the calendar from any global Stock exchange from [Pandas Market Calendars](https://pandas-market-calendars.readthedocs.io/en/latest/) which should serve our purpose. After we install pandas_market_calendars, we can import it along with other needed packages. For this project, we'll fetch 3 years back and 6 years forward for the calendar. Let's define a function called *get_market_calendar* using the exchange, start_date, end_date and timezone paramaters that returns a dataframe. We will then call the function using the *NYSE* stock exchange with our date range and using the *America/New_York* timezone.

        import datetime as dt
        import sqlalchemy as sa
        from sqlalchemy.ext.declarative import declarative_base
        import os
        import urllib.parse as url
        import pandas as pd
        import pandas_market_calendars as mcal

        def get_market_calendar(exchange, s_date, e_date, timezone):

            """
            Fetch the market calendar schedule for a given exchange.

            Args:
                exchange (str): The exchange name (e.g., 'NYSE').
                s_date (str): Start date in 'YYYY-MM-DD' format.
                e_date (str): End date in 'YYYY-MM-DD' format.
                timezone (str): Timezone for the calendar.

            Returns:
                DataFrame: DataFrame with columns Date, Open_Time, and Close_Time.
            """
    
            try:
                # Get the calendar for the specified exchange
                nyse = mcal.get_calendar(exchange)
                # Fetch the schedule for the date range
                df_tmp = nyse.schedule(start_date=s_date, end_date=e_date, tz=timezone)
        
                # Extract date, open time, and close time from market_open and market_close
                df_tmp['Date'] = pd.to_datetime(df_tmp['market_open']).dt.date
                df_tmp['Open_Time'] = pd.to_datetime(df_tmp['market_open']).dt.time
                df_tmp['Close_Time'] = pd.to_datetime(df_tmp['market_close']).dt.time
        
                # Select only relevant columns
                df_tmp = df_tmp[['Date', 'Open_Time', 'Close_Time']]
        
                return df_tmp
    
            except Exception as ex:
                print(f"Error fetching calendar data: {ex}")
                raise

            # Fetch the calendar data for the NYSE
            df_dates = get_calendar('NYSE', start_date, end_date, 'America/New_York')

Once we create a database connection, we will declare our *Market_Calendar* table. We will load the data directly into the table as this is a one-time load with respect to any future projects.

        Base = sa.orm.declarative_base()

        class Market_Calendar(Base):
    
            """
            SQLAlchemy ORM class representing the 'Market_Calendar' table in the 'Equities' schema.

            Attributes:
                __tablename__ (str): The name of the table.
                __table_args__ (dict): Additional arguments for the table, including schema name.
                Country (Column): Country or exchange code.
                Date (Column): The date of the market schedule.
                Open_Time (Column): Market open time.
                Close_Time (Column): Market close time.
            """    
    
            __tablename__ = 'Market_Calendar'
            __table_args__ = {'schema': 'Equities'}
            Country = sa.Column(sa.String, primary_key=True)
            Date = sa.Column(sa.Date, primary_key=True)
            Open_Time = sa.Column('Open_Time', sa.Time)
            Close_Time = sa.Column('Close_Time', sa.Time)

Now let's load the data into the *Market_Calendar* table for the country = "United States".  

        country = "United States" # Set the country to be United States

        # Process each row in the DataFrame
        try:
            for index, row in df_dates.iterrows():
        
                # Query the 'Market_Calendar' table to find records where the 'Country" column matches country variable and the 
                # 'Date' column matches the value in the DataFrame's 'Date' row
                q1 = s1.query(Market_Calendar).filter(Market_Calendar.Country == country, Market_Calendar.Date == row['Date'])
        
                # Check if any records were found with the specified 'Country' and 'Date'
                if (q1.count() >= 1):
                    # If one or more records are found, get the first matching record
                    q1 = s1.query(Market_Calendar).filter(Market_Calendar.Country == country, Market_Calendar.Date == row['Date']).first()
                    # Update existing record
                    q1.Open_Time = row['Open_Time']
                    q1.Close_Time = row['Close_Time']
                else:
                    # Create new record
                    q1 = Market_Calendar(
                        Country=country,
                        Date=row['Date'],
                        Open_Time=row['Open_Time'],
                        Close_Time=row['Close_Time']
                    )
                    s1.add(q1)

        # Handle SQLAlchemy errors
        except sa.exc.SQLAlchemyError as e:
            message = f"Issue with updating Market_Calendar database table for Date: {row['Date']}. Error: {e}"
            print(message)
            s1.rollback()  # Rollback changes on error
            raise

        # Commit the changes to the database
        s1.commit()

        print("Database data load is complete")

Finally, we validate if all the records were loaded.

        # Execute SQL query to count the number of records in the Market_Calendar table
        sql_stat = """SELECT COUNT(*) FROM [Financial_Securities].[Equities].[Market_Calendar]"""
        try:
            result = e.execute(sql_stat)
            cnt_recs = result.scalar()
    
        # Handle errors querying the Market_Calendar table
        except sa.exc.SQLAlchemyError as e:
            print(f"Issue querying Market_Calendar database table for count! Error: {e}")
    
        # Compare the number of records in the database with the number of records in the DataFrame
        if cnt_recs < len(df_dates):
            print(f"Only {cnt_recs} of {len(df_dates)} records were loaded into Market_Calendar database table!")
        else:
            print(f"All {cnt_recs} records were loaded into Market_Calendar database table!")  

        s1.close()  # Close the session

## Load Yahoo Equity Pricing data: *[Load-Yahoo_Equity_Prices.ipynb](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-ETL-Process/Load-Yahoo_Equity_Prices.ipynb)*

In this last process, we will load the *Yahoo_Equity_Prices* with Yahoo pricing data we staged. We connect to the database, declare the *Yahoo_Equity_Prices* table, and then create a complex query that will now merge the dates of the *Market_Calendar* with the ticker range of dates. If any prices are null, we can then handle them by forward filling them. The query data is then bound to the *df_pricing* dataframe.

        # SQL query to get the Ticker_ID, Ticker and pricing data from Data_STG and Equities tables
        # and joined with Market_Calendar to get all possible dates in case there are missing dates
        # between the bounds of the existing pricing dates for each Ticker.
        sql_stat = """WITH q1 AS 
        (SELECT
         Description, 
         CAST(MIN(Date) AS Date) AS Min_Date,
         CAST(MAX(Date) AS Date) AS Max_Date
        FROM [Financial_Securities].[Equities].[Data_STG]
        GROUP BY Description),
        q2 AS
        (SELECT
         q3.Ticker_ID,
         q3.Ticker,
         q4.Date
        FROM
        [Financial_Securities].[Equities].[Equities] q3,
        [Financial_Securities].[Equities].[Market_Calendar] q4),
        q5 AS
        (SELECT 
         q2.Ticker_ID,
         q2.Ticker,
         q2.Date 
        FROM q2
        INNER JOIN q1
        ON q1.Description = q2.Ticker
        AND q2.Date BETWEEN q1.Min_Date AND q1.Max_Date)
        SELECT 
         q5.Ticker_ID,
         q5.Ticker,
         q5.Date,
         ROUND(q7.Float_Value1, 2) AS Float_Value1,
         ROUND(q7.Float_Value2, 2) AS Float_Value2, 
         ROUND(q7.Float_Value3, 2) AS Float_Value3, 
         ROUND(q7.Float_Value4, 2) AS Float_Value4, 
         q7.Int_Value1
        FROM q5
        LEFT OUTER JOIN [Financial_Securities].[Equities].[Data_STG] q7
        ON q5.Ticker = q7.Description
        AND q5.Date = CAST(q7.Date AS Date)
        ORDER BY q5.Ticker_ID, q5.Date
        """
                                                                    
        try:              
            df_pricing = pd.read_sql(sql_stat, s1.bind) # Execute the SQL query through the session and bind the data to the df_pricing dataframe
    
        # Handle SQLAlchemy errors if they occur during query execution
        except sa.exc.SQLAlchemyError as e:
            print(f"Issue querying database tables! Error: {e}")
            s1.close()  # Close the session
            raise  # Re-raise the exception to propagate the error
    
        print("Query data load is complete")

Let's now forward fill all the pricing data based on Ticker.

        # Let's sort and forward fill any pricing data that is missing for dates in the
        # Market Calendar within the bounds of the existing pricing dates for each Ticker
        df_pricing.sort_values(by=['Ticker_ID', 'Date'], inplace=True)
        df_pricing[['Float_Value1', 'Float_Value2', 'Float_Value3', 'Float_Value4']] = df_pricing.groupby('Ticker_ID')[['Float_Value1', 'Float_Value2', 'Float_Value3', 'Float_Value4']].ffill()

We iterate through the *df_pricing* dataframe and load the *Yahoo_Equity_Prices* table.

        for index, row in df_pricing.iterrows():
            try:
        
                # Query the 'Yahoo_Equity_Prices' table to find records where the 'Date' column matches the value in the DataFrame's 'Date' row
                # and the 'Ticker_ID' column matches the value in the DataFrame's 'Ticker_ID' row
                q1 = s1.query(Yahoo_Equity_Prices).filter(Yahoo_Equity_Prices.Date == row.Date, Yahoo_Equity_Prices.Ticker_ID == row.Ticker_ID)

                # Check if any records were found with the specified 'Date' and 'Ticker_ID'
                if (q1.count() >= 1):
                    # If one or more records are found, get the first matching record
                    q1 = s1.query(Yahoo_Equity_Prices).filter(Yahoo_Equity_Prices.Date == row.Date, Yahoo_Equity_Prices.Ticker_ID == row.Ticker_ID).first()
                    # Update the pricing attributes of the found record with the values from the DataFrame's pricing columns
                    q1.Open=row['Float_Value1']
                    q1.High=row['Float_Value2']
                    q1.Low=row['Float_Value3']
                    q1.Close= row['Float_Value4']
                    q1.Volume=row['Int_Value1']
            
                else:
            
                    # Create a new Yahoo_Equity_Prices object for each row in df_pricing dataframe
                    q1 = Yahoo_Equity_Prices(
                        Ticker_ID=row['Ticker_ID'],
                        Date=row['Date'],
                        Open=row['Float_Value1'],
                        High=row['Float_Value2'],
                        Low=row['Float_Value3'],
                        Close=row['Float_Value4'],
                        Volume=row['Int_Value1']
                    )
    
                    s1.add(q1)  # Add the instance to the session
        
            # Handle SQLAlchemy errors if they occur during adding the object
            except sa.exc.SQLAlchemyError as e:
                message = f"Issue with updating Yahoo_Equity_Prices database table for Ticker: {row.Ticker}. Error: {e}"
                print(message)
                s1.close()  # Close the session
                raise  # Re-raise the exception to propagate the error

        s1.commit() # Commit the transactions to the database

        print("Database data load is complete")

And lastly, we validate if all the records have been loaded and close the session.

        # SQL query to count the number of records in the Data_STG table
        sql_stat2 = """SELECT COUNT(*) FROM [Financial_Securities].[Equities].[Data_STG]"""
          
        try: 
            result1 = e.execute(sql_stat2)  # Execute the count query
            cnt_recs1 = result1.scalar()  # Get the count of records
    
        # Handle SQLAlchemy errors if they occur during query execution
        except sa.exc.SQLAlchemyError as e:
            print(f"Issue querying Data_STG database table for count! Error: {e}")


        # SQL query to count the number of records in the Yahoo_Equity_Prices table
        sql_stat3 = """SELECT COUNT(*) FROM [Financial_Securities].[Equities].[Yahoo_Equity_Prices]"""
              
        try: 
            result1 = e.execute(sql_stat3)  # Execute the count query
            cnt_recs2 = result1.scalar()  # Get the count of records
    
        # Handle SQLAlchemy errors if they occur during query execution
        except sa.exc.SQLAlchemyError as e:   
            print(f"Issue querying Sub_Industries database table for count! Error: {e}")

        # Compare the record counts and print the result
        if cnt_recs2 < cnt_recs1:
            print(f"Only {cnt_recs2} of {cnt_recs1} records were loaded into Yahoo_Equity_Prices database table!")
        else:
            print(f"All {cnt_recs2} records were loaded into Yahoo_Equity_Prices database table!") 

        s1.close()  # Close the session

