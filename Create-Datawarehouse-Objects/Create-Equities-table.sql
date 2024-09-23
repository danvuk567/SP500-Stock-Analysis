CREATE TABLE [Financial_Securities].[Equities].[Equities](
			[Ticker_ID] [int] IDENTITY (1, 1) NOT NULL,
			[Ticker] [nchar](10) NOT NULL,
			[Name] [nchar](50) NULL,
                        [Sub_Industry_ID] [int] NOT NULL,
        	CONSTRAINT PK_Equities PRIMARY KEY(Ticker_ID));
