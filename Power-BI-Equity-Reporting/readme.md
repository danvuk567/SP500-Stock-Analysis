# Power BI Equity Reporting

## Equity Hierarchical Dimension Slicers

For the 1st report tab, we'll focus on building Pricing data visuals. 
We start by building a **Slicer** using *Sector* from the *Sectors* table and define the *Style* as *Tile*.
This will allow us to choose Equities from a particular Sector.

![Power_BI_Pricing_Sector_Slicer.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Pricing_Sector_Slicer.jpg?raw=true)

Next, we'll create 3 slicers using the *Style* as *Vertical List*, one using *Industry Group* from the *Industry_Groups* table, one using *Industry* from the *Industies* table, 
and another using *Sub_industry* from the *Sub_Industries* table. This will allow us to further filter Equities from specific Industry categories.

![Power_BI_Pricing_Industry_Group_Industry_Sub_Industry_Slicer.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Pricing_Industry_Group_Industry_Sub_Industry_Slicer.jpg?raw=true)

The last slicer will also use a *Style* as *Vertical List* and use *Ticker* from the *Equities* table. This will provide a final list of Tickers to choose from to fetch pricing data.

![Power_BI_Pricing_Tickers_Slicer.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Pricing_Tickers_Slicer.jpg?raw=true)



