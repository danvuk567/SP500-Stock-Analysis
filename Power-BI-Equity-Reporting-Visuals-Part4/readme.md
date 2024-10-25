# Power BI S&P 500 Equity Reporting Visuals - Part 4

The 4th reporting tab called *S&P 500 Equity Performance by Sub-Industry* independently visualizes Equity performance by Sub-Industry. The **Slicer** dropdown visual uses *Sector* from the *Sectors* table to filter Returns by Sub-Industry for the Sector in the other visuals.

![Power_BI_Sector_Sub_Industry_Slicer.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Sector_Sub_Industry_Slicer.jpg?raw=true)

The **Donut Chart** called *# of Tickers per Sub-Industry* simply displays the count of Tickers per Sub-Industry using *Sub_Industry* from the *Sub-Industries* table in the *Legend* and *Ticker_ID* from the *Equities* table in the *Values*.

![Power_BI_Sub_Industry_Ticker_Count_Donut_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Sub_Industry_Ticker_Count_Donut_Chart.jpg?raw=true)

The **Clustered Column Chart** called *Average % Return by Year and Sub-Industry* displays the Average of Yearly Returns by Sub-Industry using *Year* from the *Equity_Returns_by_Year* table in the *X-Axis*, the average of the *% Return* from the *Equity_Returns_by_Year* table in the *Y-Axis* and *Sub_Industry* from the *Sub_Industries* table in the *Legend*.

![Power_BI_Sub_Industry_Year_Return_Column_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Sub_Industry_Year_Return_Column_Chart.jpg?raw=true)

The last visual is a **Treemap** called *Top 5 Annualized % Return by Sub-Industry* displays the top 5 Tickers by Annualized Return and Sub-Industry. The *Sub_Industry* from the *Sub-Industries* table is used for *Category*, the *Ticker* from the *Equities* table in *Details*, *Annualized % Return* from the *Equity_Statistics* table in *Values* and *Name* from the *Equities* table in the *Tooltips*. An advanced filter is added using the *RankAnnualizedReturnsbySub_Industry* measure from the *Equity_Statistics* table with value <= 5.

![Power_BI_Sub_Industry_Treemap.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Sub_Industry_Treemap.jpg?raw=true)

Here is the final version of the *S&P 500 Equity Performance by Sector* report tab:

![Power_BI_Equity_Report_4th_tab.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Equity_Report_4th_tab.jpg?raw=true)

