# Database and Table Creation files Description

For this project, we will use an SQL server database. The sql files will create database objects needed to house our data for analysis. The files can be run in any SQL Server console or via command line. I will describe what the purpose of each file is going forward. 

Equities fall into a type of business and although every business is unique, business can be classified under industries such as manufacturing, retail, financial services etc. The most common Industry classification is the Global Industry Classification Standard (GICS) which is also used by S&P Indices. There are 4 levels of GICS industry classification: Sector, Industry Group. Industry and Sub-Industry. In order to aggregate and analyze data at higher levels, we will create these Dimension tables using some of the sql scripts described below. These tables will be part of a relational hierarchy that is linked to *Equities* Dimension table that will store the unique descriptors for our S&P 500 Equities. 

For more information on GICS industry classification, refer to these official websites: [The Global Industry Classification Standard](https://www.msci.com/our-solutions/indexes/gics) and [GICS: Global Industry Classification Standard](https://www.spglobal.com/spdji/en/landing/topic/gics/). 


## *Create Database.sql*

    CREATE DATABASE Financial_Securities;

    CREATE SCHEMA Equities;


This sql file will create the database called *Financial_Securities* which will house Financial Securities data. It will also create a schema called *Equities* which is the type of Financial Securities we will be focusing on.


## *Create Data_STG table.sql*

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

This sql file will create the Data_STG table. Before we create any tables that will store our data, It is good practice to create a staging table that will handle the types of data we will need to load. A staging table is always a good idea as it allows to for any data transformation or merging of data to occur before loading into a final table. It also allows for validating and correcting any issues that may occur. I like to create a table that handles different dates, text, integers and float values. For simplicity’s sake, I will use 5 fields for each type for now that should handle most types of data loads in the future. Financial data usually has a date and string type identifiers so we will use Data and Description for the Primary Key. If there is no date, we can always use today's date. 


## *Create Equities table.sql*

    CREATE TABLE [Financial_Securities].[Equities].[Equities](
	  [Ticker_ID] [int] IDENTITY (1, 1) NOT NULL,
	  [Ticker] [nchar](10) NOT NULL,
	  [Name] [nchar](50) NULL,
      [Sub_Industry_ID] [int] NULL,
    CONSTRAINT PK_Equities PRIMARY KEY(Ticker_ID));

This sql file will create the Equities table which will be our Dimension table with an auto-generated identity Ticker_ID, the Ticker symbol and the name of the Ticker. Equities usually belong to a Sub-Industry

