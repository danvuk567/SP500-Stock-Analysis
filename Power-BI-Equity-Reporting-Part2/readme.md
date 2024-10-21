# Power BI S&P 500 Equity Reporting - Part 2

The 2nd reporting tab called *S&P 500 Equity Performance* contains the same slicers as the 1st tab for *Sector*, *Industry Group*, *Industry*, *Sub-Industry* and *Equities* and also interacts with the 1st tab.

## Equity Return Line and Column Charts

Our Yearly Return Chart called *% Return by Year and Ticker* is defined as a **Line and Clustered Column Chart** with *Year* on the *X-Axis*, *% Return* on the *Column y-axis* and *Cumulative % Return* on the 
*Line y-axis* from the *Equity_Returns_by_Year* table. The *Ticker* is added in the *Tooltips*. 

Our Quarterly Return Chart called *% Return by Quarter and Ticker* is defined as a **Line and Clustered Column Chart** with *Quarter* on the *X-Axis*, *% Return* on the *Y-Axis* and *Cumulative % Return* from the *Equity_Returns_by_Quarter* table. The *Ticker* is added in the *Tooltips*.

Our Monthly Return Chart called *Cumulative % Return by Month and Ticker* is defined as a **Line Chart** with *Date* on the *X-Axis* and *Cumulative % Return* on the *Y-Axis* from the *Equity_Returns_by_Quarter* table. 
A Trend Line of the Cumulative % Return is shown. And the *Month* and *% Return* is added in the *Tooltips*. The *Ticker_Label* from the Equities table is added to the Legend.

Our Daily Return Chart called *Cumulative % Return by Date and Ticker* is defined as a **Line Chart** with *Date* on the *X-Axis* and *Cumulative % Return* on the *Y-Axis* from the *Equity_Returns_by_Quarter* table. 
A Trend Line of the Cumulative % Return is shown. The *Ticker_Label* from the Equities table is added to the Legend.

![Power_BI_Return_Line_Columns_Charts.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Return_Line_Columns_Charts.jpg?raw=true)

To display the performance statistics for the last Date, we'll use a **Multi-row Card** visual called *Latest Perfromance* with the metrics *% Return*, *Cumulative % Return*, *Lowest % Return*, *25th Percentile % Return*, *Median % Return*, *75th Percentile % Return*, *Highest % Return*, *Average % Return*, *Return % Variance*, *Annualized % Return*, *Annualized Volatility*, *Annualized Sharpe Ratio*, *Annualized Sortino Ratio*, *Calmar Ratio* and *Max % Drawdown* from the *Equity_Statistics* table.

![Power_BI_Return_Multi_Row_Card_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Return_Multi_Row_Card_Chart.jpg?raw=true)

Here is the final version of the *S&P 500 Equity Perfromance* report tab:

![Power_BI_Equity_Report_2nd_tab.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Equity_Report_2nd_tab.jpg?raw=true)
