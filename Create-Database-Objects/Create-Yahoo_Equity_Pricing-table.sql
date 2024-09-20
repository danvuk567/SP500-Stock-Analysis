CREATE TABLE [Financial_Securities].[Equities].[Yahoo_Equity_Prices](
            [Date] [date] NOT NULL,
			[Ticker_ID] [int] NOT NULL,
			[Open] [real] NULL,
			[High] [real] NULL,
			[Low] [real] NULL,
			[Close] [real] NULL,
			[Volume] [bigint] NULL,
			CONSTRAINT PK_US_Yahoo_Equity_Prices PRIMARY KEY([Date], [Ticker_ID]));



