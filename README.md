# **Data Analysis: S&P 500 Equities**

![Forbes Line Chart](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/stock_chart.jpg?raw=true)

## **Objective** ##

In this project, I designed and implemented a full stack workflow involving end-to-end ETL processes, analytics and visualizations. 
The focus was to transform, load and study S&P 500 Equity return data. The sections below describe, in great detail, the methodologies, 
technologies and exploratory result observations.

## **Table of Contents** ##

- [Data Sources and File Transformation Overview](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Data-Source-Files/readme.md)
- [Data Warehouse Creation File Description](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Create-Datawarehouse-Objects/readme.md)
- [Python ETL Process Description](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-ETL-Process/readme.md)
- [SQL Equity Performance Analysis](https://github.com/danvuk567/SP500-Stock-Analysis/tree/main/SQL-Equity-Performance-Analysis)
- [Python Equity Performance Analysis](https://github.com/danvuk567/SP500-Stock-Analysis/tree/main/Python-Equity-Performance-Analysis)
- [Python Portfolio Performance Analysis](https://github.com/danvuk567/SP500-Stock-Analysis/tree/main/Python-Portfolio-Performance-Analysis)
- [Python Sector/Sub-Industry Performance Analysis](https://github.com/danvuk567/SP500-Stock-Analysis/tree/main/Python-Sector-Sub_Industry-Performance-Analysis)
- [Power_BI-Equity-Data-Model-Development](https://github.com/danvuk567/SP500-Stock-Analysis/tree/main/Power_BI-Equity-Data-Model-Development)
- [Power-BI-Equity-Reporting-Visuals-Part1](https://github.com/danvuk567/SP500-Stock-Analysis/tree/main/Power-BI-Equity-Reporting-Visuals-Part1)
- [Power-BI-Equity-Reporting-Visuals-Part2](https://github.com/danvuk567/SP500-Stock-Analysis/tree/main/Power-BI-Equity-Reporting-Visuals-Part2)
- [Power-BI-Equity-Reporting-Visuals-Part3](https://github.com/danvuk567/SP500-Stock-Analysis/tree/main/Power-BI-Equity-Reporting-Visuals-Part3)
- [Power-BI-Equity-Reporting-Visuals-Part4](https://github.com/danvuk567/SP500-Stock-Analysis/tree/main/Power-BI-Equity-Reporting-Visuals-Part4)
- [Power-BI Report File](https://github.com/danvuk567/SP500-Stock-Analysis/tree/main/Power_BI-Files)

## **Free Data Sources Used** ##

- List of S&P 500 companies page (Wikipedia, as of September 2024): (https://en.wikipedia.org/w/index.php?title=List_of_S%26P_500_companies&oldid=1246399544)
- Global Industry Classification Standard (Wikipedia, as of August 2024): (https://en.wikipedia.org/w/index.php?title=Global_Industry_Classification_Standard&oldid=1243171079)
- GLOBAL INDUSTRY CLASSIFICATION STANDARD (GICS®) METHODOLOGY (MSCI): (https://www.msci.com/documents/1296102/11185224/GICS+Methodology+2020.pdf)
- S&P 500 Equities Latest Pricing data (Barchart, as of September 2024): (https://www.barchart.com/stocks/indices/sp/sp500?viewName=main)
- YFinance API: (https://pypi.org/project/yfinance/)
- Pandas Market Calendars API: (https://pandas-market-calendars.readthedocs.io/en/latest/)

## **Technologies** ##

- Language: SQL, Python, DAX
- Extraction and transformation: Excel Power Query, Jupyter Notebook
- Storage: Microsoft Azure SQL Database
- Dashboard: Power BI

## **Snowflake Schema Data Modelling** ##

This basic Snowflake schema for our small Equity Data Warehouse was designed using the principles of Dimension and Fact data modeling concepts.

![Equity_Snowflake_Schema_ERD.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/Equity_Snowflake_Schema_ERD.jpg?raw=true)



