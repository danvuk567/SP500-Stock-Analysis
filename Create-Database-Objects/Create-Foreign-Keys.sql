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