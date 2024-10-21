# Power BI S&P 500 Equity Reporting - Part 2

The 2nd reporting tab called *S&P 500 Equity Performance* contains the same slicers as the 1st tab for *Sector*, *Industry Group*, *Industry*, *Sub-Industry* and *Equities* and also interacts with the 1st tab.

## Equity Return Line Charts

Our Yearly Return Chart called *% Return by Year and Ticker* is defined as a **Line and Clustered Column Chart** with *Year* on the *X-Axis*, *% Return* on the *Column y-axis* and *Cumulative % Return* on the 
*Line y-axis* from the *Equity_Returns_by_Year* table. The *Ticker* is added in the *Tooltips*. 

Our Quarterly Return Chart called *% Return by Quarter and Ticker* is defined as a **Line and Clustered Column Chart** with *Quarter* on the *X-Axis*, *% Return* on the *Y-Axis* and *Cumulative % Return* from the *Equity_Returns_by_Quarter* table. The *Ticker* is added in the *Tooltips*.

Our Monthly Return Chart called *Cumulative % Return by Month and Ticker* is defined as a **Line Chart** with *Date* on the *X-Axis* and *Cumulative % Return* on the *Y-Axis* from the *Equity_Returns_by_Quarter* table. 
A Trend Line of the Cumulative % Return is shown. And the *Month* and *% Return* is added in the *Tooltips*. The *Ticker_Label* from the Equities table is added to the Legend.

Our Daily Return Chart called *Cumulative % Return by Date and Ticker* is defined as a **Line Chart** with *Date* on the *X-Axis* and *Cumulative % Return* on the *Y-Axis* from the *Equity_Returns_by_Quarter* table. 
A Trend Line of the Cumulative % Return is shown. The *Ticker_Label* from the Equities table is added to the Legend.

![Power_BI_Return_Line__Columns_Charts.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Power_BI_Return_Line__Columns_Charts.jpg?raw=true)
