# Data Sources and File Transformation Overview

## Finding and transforming Sub-Industry data for S&P 500 Equities

Before we can create a Dimension relational hierarchy that is linked to Equities, we'll need the S&P 500 tickers with their GICS Sub-Industry classification. Most paid financial services such as Bloomberg and Factset will have this capability and there are ways to piece together this information using free services. For the sake of simplicity and time, We can use Wikipedia and reference the List of S&P 500 companies page: [List of S&P 500 companies](https://en.wikipedia.org/w/index.php?title=List_of_S%26P_500_companies&oldid=1246399544) that was updated in September 2024. We then copy-paste and format this data in excel and save it as *SP500_GICS_Sub-Industries.csv* in the *Data_Files* folder.

![S&P500 GICS Sub-Industries Excel](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_GICS_Sub-Industries.jpg?raw=true)


## Finding and transforming Sector, Industry and Sub-Industry data

Let's reference this Wikipedia link: [Global Industry Classification Standard](https://en.wikipedia.org/w/index.php?title=Global_Industry_Classification_Standard&oldid=1243171079) that was last updated in August 2024. We then copy-paste the data into excel and use **Power Query** to clean up and transform the data and save the file as *GICS_Industries.csv* in the *Data_Files* folder.

![GICS Industries Excel](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/GICS_Industries.jpg?raw=true)


## Merging S&P 500 Sub_industry data with Power Query

We will then load *SP500_GICS_Sub-Industries.csv* and *GICS_Industries.csv* into Excel and use **Power Query** to merge the data based on Sub-Industry and save it as *SP500_GICS_Combined.csv*.

![S&P 500 GICS Combined Excel](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_GICS_Combined.jpg?raw=true)


## Finding Latest S&P 500 Equities Pricing data

Since our focus will be on Equities for this project, let's use Stocks that are components of the S&P 500 Index. One way to do this is to go to Barchart: [Barchart Website](https://www.barchart.com), create a free account and then navigate to the Indices Section and click on S&P Indices: [Barchart S&P 500 Index](https://www.barchart.com/stocks/indices/sp/sp500?viewName=main). Scroll down to the S&P 500 ETF Components section and click on download to export the csv. The file will look like: *sp-500-index-mm-dd-yyyy.csv* (mm: month, dd: day, yyyy: year). Let's rename it and save it as *SP500_Equities_Prices.csv* in the *Data_Files* folder. We will use this file to validate the *SP500_GICS_Combined.csv* file to make sure we have 2 sources that match the latest list of S&P 500 tickers.

![S&P 500 GICS Combined Excel](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Equities_Prices.jpg?raw=true)
