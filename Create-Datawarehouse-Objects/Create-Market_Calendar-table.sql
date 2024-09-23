CREATE TABLE [Financial_Securities].[Equities].[Market_Calendar](
            [Country] [nchar](30) NOT NULL,
			[Date] [date] NOT NULL,
			[Open_Time] [time] NULL,
			[Close_Time] [time] NULL,
        		CONSTRAINT PK_Market_Calendar PRIMARY KEY([Country], [Date]));


