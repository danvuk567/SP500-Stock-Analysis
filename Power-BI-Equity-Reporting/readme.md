# Power BI Equity Reporting

## Equity Hierarchical Dimension Slicers

For the 1st report tab called *S&P 500 Equity Pricing*, we'll focus on building Pricing data visuals. 
We start by building a **Slicer** using *Sector* from the *Sectors* table and define the *Style* as *Tile*.
This will allow us to choose Equities from a particular Sector.

![Power_BI_Pricing_Sector_Slicer.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Pricing_Sector_Slicer.jpg?raw=true)

Next, we'll create 3 slicers using the *Style* as *Vertical List*, one using *Industry Group* from the *Industry_Groups* table, one using *Industry* from the *Industies* table, 
and another using *Sub_industry* from the *Sub_Industries* table. This will allow us to further filter Equities from specific Industry categories.

![Power_BI_Pricing_Industry_Group_Industry_Sub_Industry_Slicer.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Pricing_Industry_Group_Industry_Sub_Industry_Slicer.jpg?raw=true)

The last slicer will also use a *Style* as *Vertical List* and use *Ticker* from the *Equities* table. This will provide a final list of Tickers to choose from to fetch pricing data.

![Power_BI_Pricing_Tickers_Slicer.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Pricing_Tickers_Slicer.jpg?raw=true)


## Equity Pricing Line Charts

Our Yearly Pricing Chart is defined as a **Line Chart** with *Year* on the *X-Axis* and *Close* on the *Y-Axis* from the *Equity_Prices_by_Year* table. We incorporate *Date*, *Open*, *High*, *Low* and *Volume* in the *Tooltips*. We'll also use *Ticker_Label* from the *Equities* table in the *Legend* which is defined a column using *Ticker* and *Name*:

    Ticker_Label = [Ticker] & " - " & [Name]
   
![Power_BI_Year_Pricing_Line_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Year_Pricing_Line_Chart.jpg?raw=true)

Our Quarterly Pricing Chart is defined as a **Line Chart** with *Quarter* on the *X-Axis* and *Close* on the *Y-Axis* from the *Equity_Prices_by_Quarter* table. We incorporate *Date*, *Open*, *High*, *Low* and *Volume* in the *Tooltips*. We'll use *Ticker_Label* from the *Equities* table in the *Legend*.

![Power_BI_Quarter_Pricing_Line_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Quarter_Pricing_Line_Chart.jpg?raw=true)

Our Monthly Pricing Chart is defined as a **Line Chart** with *Date* on the *X-Axis* and *Close* on the *Y-Axis* from the *Equity_Prices_by_Month* table. We incorporate *Date*, *Open*, *High*, *Low* and *Volume* in the *Tooltips*. We'll also use *Ticker_Label* from the *Equities* table in the *legend*. And we incorporate the *Month Short* column from the *Equity_Prices_by_Month* table in the *Tooltips* which is defined as:

      Month Short = FORMAT([Date], "MMM")

![Power_BI_Month_Pricing_Line_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Month_Pricing_Line_Chart.jpg?raw=true)

Our Daily Pricing Chart is defined as a **Line Chart** with *Date* on the *X-Axis* and *Close* on the *Y-Axis* from the *Equity_Prices* table. We incorporate *Open*, *High*, *Low* and *Volume* in the *Tooltips*. We'll also use *Ticker_Label* from the *Equities* table in the *legend*.

![Power_BI_Daily_Pricing_Line_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Daily_Pricing_Line_Chart.jpg?raw=true)
  
To display Yearly Pricing data for the last Date, we'll use a **Mulit-row Card** visual with the Yearly metrics *YearLastDate*, *YearLastOpen*, *YearLastHigh*, *YearLastLow* and *YearLastVolume* from the *Equity_Prices_by_Year* table.

To display Quarterly Pricing data for the last Date, we'll use a **Mulit-row Card** visual with the Quarterly metrics *QuarterLastDate*, *QuarterLastOpen*, *QuarterLastHigh*, *QuarterLastLow* and *QuarterLastVolume* from the *Equity_Prices_by_Quarter* table.

To display Monthly Pricing data for the last Date, we'll use a **Mulit-row Card** visual with the Monthly metrics *MonthLastDate*, *MonthLastOpen*, *MonthLastHigh*, *MonthLastLow* and *MonthLastVolume* from the *Equity_Prices_by_Month* table.

To display Daily Pricing data for the last Date, we'll use a **Mulit-row Card** visual with the Daily metrics *LastDate*, *LastOpen*, *LastHigh*, *LastLow* and *LastVolume* from the *Equity_Pricesh* table.

![Power_BI_Pricing_Multi_Row_Card_Charts.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Pricing_Multi_Row_Card_Charts.jpg?raw=true)

Here is the final version of the *S&P 500 Equity Pricing* report tab:

![Power_BI_Equity_Report_1st_tab.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Equity_Report_1st_tab.jpg?raw=true)








   




