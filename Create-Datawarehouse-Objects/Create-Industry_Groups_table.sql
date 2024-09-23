CREATE TABLE [Financial_Securities].[Equities].[Industry_Groups](
	[Industry_Group_ID] [int] NOT NULL,
	[Name] [nchar](100) NULL,
        [Sector_ID] [int] NOT NULL,
        CONSTRAINT PK_Industry_Groups PRIMARY KEY(Industry_Group_ID));
