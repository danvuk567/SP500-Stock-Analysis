
CREATE SCHEMA Equities;

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

CREATE TABLE [Financial_Securities].[Equities].[Sectors](
	[Sector_ID] [int] NOT NULL,
	[Name] [nchar](50) NOT NULL,
CONSTRAINT PK_US_Sectors PRIMARY KEY(Sector_ID));

CREATE TABLE [Financial_Securities].[Equities].[Industry_Groups](
	[Industry_Group_ID] [int] NOT NULL,
	[Name] [nchar](100) NULL,
        [Sector_ID] [int] NOT NULL,
CONSTRAINT PK_Industry_Groups PRIMARY KEY(Industry_Group_ID));

CREATE TABLE [Financial_Securities].[Equities].[Industries](
	[Industry_ID] [int] NOT NULL,
	[Name] [nchar](100) NULL,
        [Industry_Group_ID] [int] NOT NULL,
CONSTRAINT PK_Industries PRIMARY KEY(Industry_ID));

CREATE TABLE [Financial_Securities].[Equities].[Sub_Industries](
	[Sub_Industry_ID] [int] NOT NULL,
	[Name] [nchar](100) NULL,
        [Industry_ID] [int] NOT NULL,
CONSTRAINT PK_Sub_Industries PRIMARY KEY(Sub_Industry_ID));

CREATE TABLE [Financial_Securities].[Equities].[Equities](
	[Ticker_ID] [int] IDENTITY (1, 1) NOT NULL,
	[Ticker] [nchar](10) NOT NULL,
	[Name] [nchar](50) NULL,
  [Sub_Industry_ID] [int] NOT NULL,
CONSTRAINT PK_Equities PRIMARY KEY(Ticker_ID));

CREATE TABLE [Financial_Securities].[Equities].[Yahoo_Equity_Prices](
            [Date] [date] NOT NULL,
	    [Ticker_ID] [int] NOT NULL,
	    [Open] [real] NULL,
	    [High] [real] NULL,
	    [Low] [real] NULL,
	    [Close] [real] NULL,
	    [Volume] [bigint] NULL,
CONSTRAINT PK_US_Yahoo_Equity_Prices PRIMARY KEY([Date], [Ticker_ID]));

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

CREATE TABLE [Financial_Securities].[Equities].[Market_Calendar](
            [Country] [nchar](30) NOT NULL,
	    [Date] [date] NOT NULL,
	    [Open_Time] [time] NULL,
	    [Close_Time] [time] NULL,
CONSTRAINT PK_Market_Calendar PRIMARY KEY([Country], [Date]));

