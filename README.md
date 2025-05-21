# **Data Transformation and Analysis: S&P 500 Stock Prices and Performance**

![Forbes Line Chart](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/stock_chart.jpg?raw=true)

## :pushpin: **Objective** ##

In this project, I designed and implemented a full stack workflow involving end-to-end ETL processes, analytics and visualizations. 
The focus was to transform, load and study S&P 500 Equity return data from Jan 1st, 2021 to Sep 20, 2024. 
The sections below describe, in great detail, the methodologies, technologies and exploratory result observations.

## :high_brightness: **Highlights** ##

* NVDA (Nvidia Corporation) was in the top 4 yearly returns in all 4 years from Jan 1st, 2021, to Sep 20, 2024, except in 2022.
* SMCI (Super Micro Computer, Inc) had the highest annualized return of 105.13% from Jan 1st, 2021, to Sep 20, 2024, but also had the highest annualized volatility of 72.64%.
* LLY (Eli Lilly and Company) had the highest risk-adjusted return performance measures with an Annualized Sharpe Ratio of 1.87, Annualized Sortino Ratio of 3.1 and Calmar Ratio of 1.41.
* With respect to industry sector return performance, equally weighted average returns of all stocks from Jan 1st, 2021, to Sep 20, 2024, within their respective industry Sector were used.
  Overall, the Information Technology sector was in the top 4 performing sectors in all 4 years except 2022.
  The Energy sector had the highest Annualized Return of 26.72% but also had the highest Annualized Volatility of 31.14%.
  The Consumer Staples sector had a zero (0.03%) Annualized Return but also had the lowest Annualized Volatility of 14.32%.
  
## :bookmark_tabs: **Table of Contents** ##

* [Data Sources and File Transformation Overview](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Data-Source-Files/readme.md)
* [Data Warehouse Creation File Description](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Create-Datawarehouse-Objects/readme.md)
* [Python ETL Process Description](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-ETL-Process/readme.md)
* [SQL Equity Performance Analysis](https://github.com/danvuk567/SP500-Stock-Analysis/tree/main/SQL-Equity-Performance-Analysis)
* [Python Equity Performance Analysis](https://github.com/danvuk567/SP500-Stock-Analysis/tree/main/Python-Equity-Performance-Analysis)
* [Python Portfolio Performance Analysis](https://github.com/danvuk567/SP500-Stock-Analysis/tree/main/Python-Portfolio-Performance-Analysis)
* [Python Sector/Sub-Industry Performance Analysis](https://github.com/danvuk567/SP500-Stock-Analysis/tree/main/Python-Sector-Sub_Industry-Performance-Analysis)
* [Power BI Equity Performance Analysis](https://github.com/danvuk567/SP500-Stock-Analysis/tree/main/Power_BI-Equity-Performance-Analysis)

## :link: **Free Data Sources Used** ##

* List of S&P 500 companies page (Wikipedia, as of September 2024): (https://en.wikipedia.org/w/index.php?title=List_of_S%26P_500_companies&oldid=1246399544)
* Global Industry Classification Standard (Wikipedia, as of August 2024): (https://en.wikipedia.org/w/index.php?title=Global_Industry_Classification_Standard&oldid=1243171079)
* GLOBAL INDUSTRY CLASSIFICATION STANDARD (GICS®) METHODOLOGY (MSCI): (https://www.msci.com/documents/1296102/11185224/GICS+Methodology+2020.pdf)
* S&P 500 Equities Latest Pricing data (Barchart, as of September 2024): (https://www.barchart.com/stocks/indices/sp/sp500?viewName=main)
* YFinance API: (https://pypi.org/project/yfinance/)
* Pandas Market Calendars API: (https://pandas-market-calendars.readthedocs.io/en/latest/)

## :computer: **Technologies** ##

* Language: SQL, Python, DAX
* Extraction and data transformation: Excel Power Query, Jupyter Notebook
* Storage: Microsoft Azure SQL Database
* Dashboard: Power BI

## **Snowflake Schema Data Modelling** ##

This basic Snowflake schema for our small Equity Data Warehouse was designed using the principles of Dimension and Fact data modeling concepts.<br/><br/>

:arrow_right: **Back to:** [Main Page](https://github.com/danvuk567)

![Equity_Snowflake_Schema_ERD.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Equity_Snowflake_Schema_ERD.jpg?raw=true)



