CREATE TABLE [Financial_Securities].[Equities].[Sub_Industries](
	[Sub_Industry_ID] [int] NOT NULL,
	[Name] [nchar](100) NULL,
        [Industry_ID] [int] NOT NULL,
        CONSTRAINT PK_Sub_Industries PRIMARY KEY(Sub_Industry_ID));
