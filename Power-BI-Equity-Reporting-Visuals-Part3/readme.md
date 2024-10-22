# Power BI S&P 500 Equity Reporting Visuals - Part 3

The 3rd reporting tab called *S&P 500 Equity Performance by Sector* independently visualizes Equity performance by Sector. The **Donut Chart** called *# of S&P 500 Equities per Sector* simply displays the count of Tickers per Sector using *Sector* from the *Sectors* table in the *Legend* and *Ticker_ID* from the *Equities* table in the *Values*.

![Power_BI_Sector_Ticker_Count_Donut_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Sector_Ticker_Count_Donut_Chart.jpg?raw=true)

The **Clustered Column Chart** called *Average % Return by Year and Sector* displays the Average of Yearly Returns by Sector using *Year* from the *Equity_Returns_by_Year* table in the *X-Axis*, the average of the *% Return* from the *Equity_Returns_by_Year* table in the *Y-Axis* and *Sector* from the *Sectors* table in the *Legend*.

![Power_BI_Sector_Year_Return_Column_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Sector_Year_Return_Column_Chart.jpg?raw=true)

The **Funnel Chart** called *Top 10 Annualized % Returns* displays the top 10 Tickers by Annualized Return. It did not fit in our *S&P 500 Equity Performance* tab but can be compared to the *Top 5 Annualized % Return by Sector* visual. The *Ticker* from the *Equities* table is used for *Category*, *Annualized % Return* from the *Equity_Statistics* table in *Values* and *Name* from the *Equities* table in the *Tooltips*. We use a *Filter* with *Top N* type as 10 for *Annualized % Return* from the *Equity_Statistics* table.

![Power_BI_Equity_Funnel_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Equity_Funnel_Chart.jpg?raw=true)

The last visual is a **Treemap** called *Top 5 Annualized % Return by Sector* displays the top 5 Tickers by Annualized Return and Sector. The *Sector* from the *Sectors* table is used for *Category*, the *Ticker* from the *Equities* table in *Details*, *Annualized % Return* from the *Equity_Statistics* table in *Values* and *Name* from the *Equities* table in the *Tooltips*.
An advanced filter is added using the *RankAnnualizedReturnsbySector* measure value <= 5.

![Power_BI_Sector_Treemap.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Sector_Treemap.jpg?raw=true)

Here is the final version of the *S&P 500 Equity Performance by Sector* report tab:

![Power_BI_Equity_Report_3nd_tab.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Equity_Report_3nd_tab.jpg?raw=true)
