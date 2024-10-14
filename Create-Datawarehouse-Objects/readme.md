# Data Warehouse Creation File Description

For this project, we will use an **Azure SQL database**. You will need a Microsoft account to log into the Azure portal: [Microsoft Azure](https://portal.azure.com/) and create an Azure Subscription. You will need to create a **Resource Group** and we can call it **FINSEC**. To create a resource for the database, we’ll search for “Azure SQL” and create a **DTU (Database Transaction Unit)** model with a **Standard Service Tier** and 250G of storage. Azure will then prompt you to create a new **SQL Server resource** and specify a server name, admin username and password, and region. For this project, I set up the **server name** as **danvuk**. After setting up the server, you will need to configure the database resource which we can name **Financial_Securities**. Our resource group now has 2 resources, the server and the database. For more information on working with Azure, this link provides some great demo videos: [Getting Started with Azure demo series](https://azure.microsoft.com/en-us/get-started/on-demand/)

![Microsoft_Azure_Subscription.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Microsoft_Azure_Subscription.jpg?raw=true)

We can use **SSMS (SQL Server Management Studio)** to connect to the Azure database, create our database objects and query our data. For more information on SSMS, refer to this link: [What is SQL Server Management Studio (SSMS)?](https://learn.microsoft.com/en-us/sql/ssms/sql-server-management-studio-ssms?view=sql-server-ver16).

![Microsoft_Azure_Database_SSMS.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Microsoft_Azure_Database_SSMS.jpg?raw=true)

The SQL file described below will create database objects in our small **Data Warehouse** using a **Snowflake schema**. For more information on Snowflake schemas, you can reference this site: [Snowflake Schema in Data Warehouse Model](https://www.geeksforgeeks.org/snowflake-schema-in-data-warehouse-model/). I will describe what the purpose of each step is going forward. 

Equities fall into a type of business and although every business is unique, businesses can be grouped and classified with similar criteria as industries such as manufacturing, retail, financial services etc. The most common Industry classification is the **Global Industry Classification Standard (GICS)** which is also used by S&P Indices. There are 4 levels of GICS industry classification: **Sector**, **Industry Group**, **Industry** and **Sub-Industry**. For more information on GICS industry classification, refer to these official websites: [The Global Industry Classification Standard](https://www.msci.com/our-solutions/indexes/gics) and [GICS: Global Industry Classification Standard](https://www.spglobal.com/spdji/en/landing/topic/gics/). In order to aggregate and analyze data at higher levels, we can create these Dimension tables using some of the **DDL** statements described below. These tables will be part of a relational hierarchy that is linked to the *Equities* **Dimension table** that stores the unique information for our S&P 500 Equities. Below are the steps described in the sql file: 


## *[Create-Data-Warehouse-Objects.sql](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Create-Datawarehouse-Objects/Create-Data-Warehouse-Objects.sql)*  

This DDL statement will create a schema called *Equities* in the *Financial_Securities* database focused on the type of Financial Securities we will be working with.

    CREATE SCHEMA Equities;


This DDL statement creates the *Data_STG* table. Before we create any tables that will store our data, it is good practice to create a staging table that will handle the types of data we will need to load. A staging table is always a good idea as it allows to for any data transformation or merging of data to occur before loading into a final table. It also allows for validating and correcting any issues that may occur. I like to create a table that handles different dates, text, integers and float values. For simplicity’s sake, I will use 5 fields for each type for now that should handle most types of data loads in the future. Financial data usually has date and string type identifiers so we will use *Data* and *Description* for the **Primary Key**. If there is no date, we can always use today's date. 

    CREATE TABLE [Financial_Securities].[Equities].[Data_STG](
      [Date] [datetime] NOT NULL,
      [Date2] [datetime] NULL,
	  [Date3] [datetime] NULL,
	  [Date4] [datetime] NULL,
	  [Date5] [datetime] NULL,
      [Description] [nchar](100) NOT NULL,
      [Description2] [nchar](100) NULL,
      [Description3] [nchar](100) NULL,
	  [Description4] [nchar](100) NULL,
	  [Description5] [nchar](100) NULL,
      [Int_Value1] [bigint] NULL,
      [Int_Value2] [bigint] NULL,
      [Int_Value3] [bigint] NULL,
	  [Int_Value4] [bigint] NULL,
	  [Int_Value5] [bigint] NULL,
      [Float_Value1] [real] NULL,
      [Float_Value2] [real] NULL,
      [Float_Value3] [real] NULL,
	  [Float_Value4] [real] NULL,
	  [Float_Value5] [real] NULL
    CONSTRAINT PK_Data_STG PRIMARY KEY(Date, Description));


This DDL statement will create the Dimension table called *Sectors* which stores GICS Sector information and is the top of the Equities relational hierarchy. The Primary Key is defined as *Sector_ID* which is unique.

    CREATE TABLE [Financial_Securities].[Equities].[Sectors](
	  [Sector_ID] [int] NOT NULL,
	  [Name] [nchar](50) NOT NULL,
    CONSTRAINT PK_US_Sectors PRIMARY KEY(Sector_ID));
    

This DDL statement will create the Dimension table called *Industry_Groups* which stores GICS Industry Group information and is one level below Sectors in the Equities relational hierarchy. *Sector_ID* stores the unique Sector identifier that the Industry Group belongs to. The Primary Key is defined as *Industry_Group_ID* which is unique.

    CREATE TABLE [Financial_Securities].[Equities].[Industry_Groups](
	  [Industry_Group_ID] [int] NOT NULL,
	  [Name] [nchar](100) NULL,
      [Sector_ID] [int] NOT NULL,
    CONSTRAINT PK_Industry_Groups PRIMARY KEY(Industry_Group_ID));


This DDL statement will create the Dimension table called *Industries* which stores GICS Industry information and is one level below Industry Groups in the Equities relational hierarchy. *Industry_Group_ID* stores the unique Industry Group identifier that the Industry belongs to. The Primary Key is defined as *Industry_ID* which is unique.

    CREATE TABLE [Financial_Securities].[Equities].[Industries](
	  [Industry_ID] [int] NOT NULL,
	  [Name] [nchar](100) NULL,
      [Industry_Group_ID] [int] NOT NULL,
    CONSTRAINT PK_Industries PRIMARY KEY(Industry_ID));


This DDL statement will create the Dimension table called *Sub_Industries* which stores GICS Sub-Industry information and is one level below Industries in the Equities relational hierarchy. *Industry_ID* stores the unique Industry identifier that the Sub-Industry belongs to. The Primary Key is defined as *Sub_Industry_ID* which is unique.

    CREATE TABLE [Financial_Securities].[Equities].[Sub_Industries](
	  [Sub_Industry_ID] [int] NOT NULL,
	  [Name] [nchar](100) NULL,
      [Industry_ID] [int] NOT NULL,
    CONSTRAINT PK_Sub_Industries PRIMARY KEY(Sub_Industry_ID));


This DDL statement will create the Dimension table called *Equities* with an auto-generated identity *Ticker_ID*, the *Ticker* symbol and the *Name* of the Ticker. *Sub_Industry_ID* stores the unique Sub-Industry identifier that the Equity belongs to. The Primary Key is *Ticker_ID* which is unique.

    CREATE TABLE [Financial_Securities].[Equities].[Equities](
	  [Ticker_ID] [int] IDENTITY (1, 1) NOT NULL,
	  [Ticker] [nchar](10) NOT NULL,
	  [Name] [nchar](50) NULL,
      [Sub_Industry_ID] [int] NOT NULL,
    CONSTRAINT PK_Equities PRIMARY KEY(Ticker_ID));


This DDL statement will create the **Fact table** called *Yahoo_Equity_Pricing* which stores the Equity pricing data extracted from Yahoo Finance. The *Ticker_ID* is the same unique Ticker identifier in the *Equities* table. Pricing data is represented by Open, High, Low, Close and Volume. For more information about these data points, you can reference this site: [Understanding an OHLC Chart and How to Interpret It](https://www.investopedia.com/terms/o/ohlcchart.asp). The Primary Key is defined as a unique composite key using *Date* and *Ticker_ID*.

    CREATE TABLE [Financial_Securities].[Equities].[Yahoo_Equity_Prices](
	  [Date] [date] NOT NULL,
	  [Ticker_ID] [int] NOT NULL,
      [Open] [real] NULL,
	  [High] [real] NULL,
	  [Low] [real] NULL,
	  [Close] [real] NULL,
	  [Volume] [bigint] NULL,
    CONSTRAINT PK_US_Yahoo_Equity_Prices PRIMARY KEY([Date], [Ticker_ID]));


These DDL statements will create the **Foreign Keys** called *FK_Industry_Groups_Sector*, *FK_Industries_Industry_Groups*, *FK_Sub_Industries_Industries*, and *FK_Equities_Sub_Industries* which will enforce a Snowflake relational hierarchy for Equities. The foreign key *FK_US_Yahoo_Equity_Prices_Ticker_ID* will link the *Equities* Dimension table to the *Yahoo_Equity_Prices* Fact table via *Ticker_ID*. These statements should only be run once the data is populated in the tables described above to ensure the constraint validation does not fail due to missing data.

	ALTER TABLE [Financial_Securities].[Equities].[Industry_Groups]
	ADD CONSTRAINT FK_Industry_Groups_Sector 
	FOREIGN KEY (Sector_ID)
	REFERENCES [Financial_Securities].[Equities].Sectors (Sector_ID);

	ALTER TABLE [Financial_Securities].[Equities].[Industries]
	ADD CONSTRAINT FK_Industries_Industry_Groups 
	FOREIGN KEY (Industry_Group_ID)
	REFERENCES [Financial_Securities].[Equities].Industry_Groups (Industry_Group_ID);

	ALTER TABLE [Financial_Securities].[Equities].[Sub_Industries]
	ADD CONSTRAINT FK_Sub_Industries_Industries 
	FOREIGN KEY (Industry_ID)
	REFERENCES [Financial_Securities].[Equities].Industries(Industry_ID);

    ALTER TABLE [Financial_Securities].[Equities].[Equities]
	ADD CONSTRAINT FK_Equities_Sub_Industries
	FOREIGN KEY FOREIGN KEY (Sub_Industry_ID)
	REFERENCES [Financial_Securities].[Equities].Sub_Industries(Sub_Industry_ID);

	ALTER TABLE [Financial_Securities].[Equities].[Yahoo_Equity_Prices]
	ADD CONSTRAINT FK_US_Yahoo_Equity_Prices_Ticker_ID 
	FOREIGN KEY (Ticker_ID)
	REFERENCES [Financial_Securities].[Equities].Equities (Ticker_ID);


This DDL statement will create the Dimension table called *Market_Calendar*. To determine if there is missing Equity pricing data in the *Yahoo_Equity_Pricing* table for any Ticker, we need to validate it against valid US market dates. The Python package [pandas_market_calendars](https://pandas-market-calendars.readthedocs.io/en/latest/) can retrieve the calendar from any global stock exchange which should serve our purpose. We can then store the date and times for any *Country* in this table. The Primary Key is defined as a unique composite key using *Country* and *Date*.

    CREATE TABLE [Financial_Securities].[Equities].[Market_Calendar](
      [Country] [nchar](30) NOT NULL,
	  [Date] [date] NOT NULL,
	  [Open_Time] [time] NULL,
	  [Close_Time] [time] NULL,
    CONSTRAINT PK_Market_Calendar PRIMARY KEY([Country], [Date]));


And there you have it! We have set up a basic Snowflake schema for our small Equity Data Warehouse.

![Equity_Snowflake_Schema_ERD.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Equity_Snowflake_Schema_ERD.jpg?raw=true)














