CREATE TABLE [Financial_Securities].[Equities].[Industries](
	[Industry_ID] [int] NOT NULL,
	[Name] [nchar](100) NULL,
        [Industry_Group_ID] [int] NOT NULL,
        CONSTRAINT PK_Industries PRIMARY KEY(Industry_ID));