CREATE TABLE [Financial_Securities].[Equities].[Industries](
	[Industry_ID] [int] NOT NULL,
	[Name] [nchar](100) NULL,
        [Industry_Group_ID] [int] NOT NULL,
        CONSTRAINT PK_Industries PRIMARY KEY(Industry_ID),
        CONSTRAINT FK_Industries_Industry_Groups FOREIGN KEY (Industry_Group_ID)
        REFERENCES [Financial_Securities].[Equities].Industry_Groups (Industry_Group_ID));