# Python Sector/Sub-Industry Performance Analysis Description

Let's do some analysis on a Sectors and Sub-Industries. We will also be adding a new function to our *custom_python_functions.py* file which can be re-used in this project. 

## Modify custom re-usable functions: *[custom_python_functions.py](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Custom-Python-Functions/custom_python_functions.py)*

Let's define a function called *scatter_plot* which will plot a **Scatter Plot** of the our returns. It usese the **matplotlib** and **sklearn** packages, and draws a **Regression Line** to predict future outcomes. The function requires a returns dataframe and return type as input parameters.

        def scatter_plot(df_tmp, return_type):

            """
            Plots a scatter plot of return.
    
            Args:
                - df_tmp: DataFrame containing return data.
                - return_type: A string representing the column name containing the returns.
            """

            # Create a scatter plot
            plt.figure(figsize=(10, 6))
            sns.scatterplot(x='Date', y=return_type, data=df_tmp)

            # Fit a linear regression model
            X = np.array(range(len(df_tmp))).reshape(-1, 1)  # Dates as numerical values
            y = df_tmp[return_type].values
            model = LinearRegression()
            model.fit(X, y)
            predicted = model.predict(X)

            # Plot the regression line
            plt.plot(df_tmp['Date'], predicted, color='red', linewidth=2, label='Regression Line')

            # Add labels and title
            plt.title(f'{return_type} with Regression Line')
            plt.xlabel('Date')
            plt.ylabel(f'{return_type}')
            plt.legend()
            plt.show()


## Sector / Sub-Industry Performance Analysis: *[Sector-Sub_Industry-Performance-Analysis.ipynb](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-Portfolio-Performance-Analysis/Sector-Sub_Industry-Performance-Analysis.ipynb)*

Let's go ahead and analyze returns aggregated by Sector from the S&P 500 Tickers. We will import the necessary packages, connect to the database and query the database for our Ticker pricing data along with our GICS Industry Classification columns that includes Sector, Industry Group, Industry, and Sub-Industry. We will then bind it to the df_pricing dataframe.

Let's look out how many unique Sectors, Industry Groups, Indistries and Sub-Industries we have.

         df_pricing_cnt = pd.DataFrame({
             '# of Sectors': [df_pricing['Sector'].nunique()],
             '# of Industry Groups': [df_pricing['Industry_Group'].nunique()],
             '# of Industries': [df_pricing['Industry'].nunique()],
             '# of Sub-Industries': [df_pricing['Sub_Industry'].nunique()]
         })

         print(df_pricing_cnt.to_string(index=False))

![SP500_GICS_Industry_Columns_Count_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_GICS_Industry_Columns_Count_Python.jpg?raw=true)

There are 11 Sectors, 25 Industry Groups, 66 Industries and 110 Sub-Industries that we have pricing data for.

How may Tickers exist by Sector? How many have positive Cumulative % Returns? How many have negative Cumulative % Returns? Let's calculate the returns and aggregate the results.

         df_ret = calculate_return(df_pricing.copy(), 'Daily')
         df_ret.sort_values(by=['Ticker', 'Date'], inplace=True)

         df_ret_last = df_ret.copy().groupby('Ticker').tail(1)

         df_ret_cnt = df_ret_last.groupby('Sector').agg(
             **{
                 '# of Tickers': ('Ticker', 'nunique'),
                 '# of Positive Cumulative Returns (%)': ('Cumulative % Return', lambda x: round(((x > 0).sum() / len(x)) * 100, 2)),
                 '# of Negative Cumulative Returns (%)': ('Cumulative % Return', lambda x: round(((x < 0).sum() / len(x)) * 100, 2))
             }
         ).reset_index()

         print(df_ret_cnt.to_string(index=False))

![SP500_GICS_Sector_Ticker_Return_Count_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_GICS_Sector_Ticker_Return_Count_Python.jpg?raw=true)

It looks like **Communication Services**, which had the smallest count of Tickers, had the lowest % of # of positive Cumulative % Returns of all Sectors at **47.86%**. There were more negative Cumulative Returns than positive. The **Energy** Sector** was the only Sector that had **100%** of # of positive Cumulative % Returns. There were no Tickers with negative Cumulative % Returns in the past 4 years.

Now, let's look at Cumulative % Return, Annualized % Return, Annualized Volatility and Annualized Downside Volatility of the different Sectors. We do this by grouping the Tickers in each Sector as a portfolio and using our custom function *calculate_portfolio_return* that aggregates average log returns from the dataframe *df_ret* to calculate these measures. We will concatenate all portfolio return measures into one dataframe *df_ret_sectors*. We then print the results for the last date.

         df_ret.sort_values(by=['Sector', 'Ticker', 'Date'], inplace=True)
         df_ret_sectors = pd.DataFrame()  # Initialize an empty DataFrame for concatenation

         # Iterate through unique sectors
         for sector in df_ret['Sector'].unique():
             # Filter the DataFrame for the current sector
             df_ret_sector_tickers = df_ret[df_ret['Sector'] == sector].copy()
             df_ret_sector_tickers.sort_values(by=['Ticker','Date'], inplace=True)

             # Call your function to calculate portfolio return
             df_ret_sector = calculate_portfolio_return(df_ret_sector_tickers.copy(), ['Sector', 'Industry_Group', 'Industry', 'Sub_Industry', 'Ticker'], 'Daily')
    
             # Add the Sector column
             df_ret_sector['Sector'] = sector
    
             # Concatenate the results
             df_ret_sectors = pd.concat([df_ret_sectors, df_ret_sector], ignore_index=True)
    
         df_ret_sectors.sort_values(by=['Sector', 'Date'], inplace=True)

         df_ret_sectors_last = df_ret_sectors.copy().groupby('Sector').tail(1)
         df_ret_sectors_last = df_ret_sectors_last[['Sector', 'Cumulative % Return', 'Annualized % Return',  'Annualized Volatility',  'Annualized Downside Volatility']]

         print(df_ret_sectors_last.to_string(index=False))

![SP500_GICS_Sector_Returns_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_GICS_Sector_Returns_Python.jpg?raw=true)

We can see that the **Consumer Staples** Sector had the lowest Annualized % Return of **-2.55%** but with lowest Annualized Volatility of **14.86%*. **Consumer Staples** stocks are not growth stocks and are usually a safe haven during economic downturns and/or used for more consistent returns and dividends. That is why they don't typically reflect high volatility. Over the past 4 years, the economy exhibited resiliance and periods of strong growth causing stronger investments in other Sectors. We see that the **Energy** Sector had the highest Annualized % Return of **25.58%** but came at a cost of highest Annulaized Downside Volatility of **22.35%**. The **Energy** Sector is often subject to significant discrepancies in supply and demand for oil and gas, leading to volatile price fluctuations, particularly during economic downturns or geopolitical risks.

We can show the Sector Cumulative % Return impact in a **Bubble Chart** using our custom function *plot_returns_bubble_chart*.

         plot_returns_bubble_chart(df_ret_sectors_last, 'Annualized % Return', 'Cumulative % Return', 'Sector', False, 0)

![SP500_GICS_Sector_Cumulative_Returns_Bubble_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_GICS_Sector_Cumulative_Returns_Bubble_Chart.jpg?raw=true)

Let's plot the Cumulative % Returns by Sector in a **Line Chart** to show how the Returns were compounded over time using our custom function *plot_returns_line_chart*.

         plot_returns_line_chart(df_ret_sectors, 'Daily', 'Cumulative % Return', 'Sector')

![SP500_GICS_Sector_Cumulative_Returns_Line_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_GICS_Sector_Cumulative_Returns_Line_Chart.jpg?raw=true)

 The **Energy** Sector clearly outperformed all Sectors but also experiencing a number of large drawdowns clearly exhibiting high volatility.

Let's now take a look at determining how a Sector is trending over the past 4 years. We can plot a **Linear Regression** line using the Cumulative % Returns and plot it on a **Line Chart**. The steeper the slope, the stronger the positive or negative trend. We'll use our custom function *scatter_plot* to plot a **Scatter Plot** and regression line for the **Consumer Staples** Sector.

        sector = 'Consumer Staples'
        df_ret_sector = df_ret_sectors[df_ret_sectors['Sector'] == sector].copy()
        scatter_plot(df_ret_sector, 'Cumulative % Return')

![SP500_GICS_Consumer_Staples Sector_Cumulative_Return_Regression_Line_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_GICS_Consumer_Staples_Sector_Cumulative_Return_Regression_Line_Chart.jpg?raw=true)

We can observe that the **Consumer Staples** Sector is in a weak negative trend.

Let's compare it to the **Energy** Sector.

        sector = 'Energy'
        df_ret_sector = df_ret_sectors[df_ret_sectors['Sector'] == sector].copy()
        scatter_plot(df_ret_sector, 'Cumulative % Return')

![SP500_GICS_Energy_Sector_Cumulative_Return_Regression_Line_Chart.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_GICS_Energy_Sector_Cumulative_Return_Regression_Line_Chart.jpg?raw=true)

We can observe that the **Energy** Sector is in a fairly stong positive trend.

And finally, let's look at Cumulative % Returns for Sub-Industries and observe the strongest performing. We can plot the top 20 Sub-Industries and highlight the top 10 in a **Bubble Chart** using our custom plot_returns_bubble_chart function.

        df_ret.sort_values(by=['Sector', 'Sub_Industry','Ticker', 'Date'], inplace=True)
        df_ret_sub_industries = pd.DataFrame()  # Initialize an empty DataFrame for concatenation

        # Iterate through unique sub-industries
        for sub_industry in df_ret['Sub_Industry'].unique():
            # Filter the DataFrame for the current sector
            df_ret_sub_industry_tickers = df_ret[df_ret['Sub_Industry'] == sub_industry].copy()
            sector = df_ret_sub_industry_tickers['Sector'].unique()[0]
            df_ret_sub_industry_tickers.sort_values(by=['Ticker','Date'], inplace=True)
    
            # Call your function to calculate portfolio return
            df_ret_sub_industry = calculate_portfolio_return(df_ret_sub_industry_tickers.copy(), ['Sector', 'Industry_Group', 'Industry', 'Sub_Industry', 'Ticker'], 'Daily')
    
            # Add the Sector column
            df_ret_sub_industry['Sector'] = sector
            df_ret_sub_industry['Sub_Industry'] = sub_industry
    
            # Concatenate the results
            df_ret_sub_industries = pd.concat([df_ret_sub_industries, df_ret_sub_industry], ignore_index=True)
    
        df_ret_sub_industries.sort_values(by=['Sector', 'Sub_Industry', 'Date'], inplace=True)

        df_ret_sub_industries_last = df_ret_sub_industries.copy().groupby(['Sector', 'Sub_Industry']).tail(1)
        df_ret_sub_industries_last = df_ret_sub_industries_last[['Sector', 'Sub_Industry', 'Date', 'Cumulative % Return', 'Annualized % Return']]
        df_ret_sub_industries_last.sort_values(by=['Sector', 'Sub_Industry'], inplace=True)

        df_ret_sub_industries_last.loc[:, 'Cumulative % Return Rank'] = df_ret_sub_industries_last.groupby('Date')['Cumulative % Return'].rank(ascending=False, method='dense').astype(int)
        num_of_ranks = 20
        df_ret_sub_industries_last_top = df_ret_sub_industries_last[df_ret_sub_industries_last['Cumulative % Return Rank'] <= num_of_ranks].copy()
        df_ret_sub_industries_last_top = df_ret_sub_industries_last_top[['Sector', 'Sub_Industry', 'Annualized % Return', 'Cumulative % Return', 'Cumulative % Return Rank']]
        df_ret_sub_industries_last_top.sort_values(by=['Cumulative % Return Rank'], inplace=True)

        plot_returns_bubble_chart(df_ret_sub_industries_last_top, 'Annualized % Return', 'Cumulative % Return', 'Sub_Industry', True, 10)

![SP500_GICS_Sub_Industries_Cumulative_Returns_Bubble_Chart_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_GICS_Sub_Industries_Cumulative_Returns_Bubble_Chart_Python.jpg?raw=true)

We can see that 4 out the top 10 Sub-Industries belong to the **Energy Sector** which makes sense.

What were the top 5 Sub-Industries in the **Energy** Sector?

        sector = 'Energy'
        df_ret_sub_industries_last2 = df_ret_sub_industries_last[df_ret_sub_industries_last['Sector'] == sector].copy()

        df_ret_sub_industries_last2.loc[:, 'Cumulative % Return Rank'] = df_ret_sub_industries_last2.groupby('Date')['Cumulative % Return'].rank(ascending=False, method='dense').astype(int)
        num_of_ranks = 5
        df_ret_sub_industries_last2_top = df_ret_sub_industries_last2[df_ret_sub_industries_last2['Cumulative % Return Rank'] <= num_of_ranks].copy()
        df_ret_sub_industries_last2_top = df_ret_sub_industries_last2_top[['Sector', 'Sub_Industry', 'Cumulative % Return', 'Cumulative % Return Rank']]
        df_ret_sub_industries_last2_top.sort_values(by=['Cumulative % Return Rank'], inplace=True)

        print(df_ret_sub_industries_last2_top.to_string(index=False))

![SP500_GICS_Energy_Sector_Sub_Industries_Top_5_Cumulative_Returns_Data_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_GICS_Energy_Sector_Sub_Industries_Top_5_Cumulative_Returns_Data_Python.jpg?raw=true)

The **Energy Oil & Gas Storage & Transportation** Sub-Industry had the strongest Cumulative % Return in the **Energy** Sector.

What were the top 5 Sub-Industries in the **Consumer Staples** Sector?

        sector = 'Consumer Staples'
        df_ret_sub_industries_last2 = df_ret_sub_industries_last[df_ret_sub_industries_last['Sector'] == sector].copy()

        df_ret_sub_industries_last2.loc[:, 'Cumulative % Return Rank'] = df_ret_sub_industries_last2.groupby('Date')['Cumulative % Return'].rank(ascending=False, method='dense').astype(int)
        num_of_ranks = 5
        df_ret_sub_industries_last2_top = df_ret_sub_industries_last2[df_ret_sub_industries_last2['Cumulative % Return Rank'] <= num_of_ranks].copy()
        df_ret_sub_industries_last2_top = df_ret_sub_industries_last2_top[['Sector', 'Sub_Industry', 'Cumulative % Return', 'Cumulative % Return Rank']]
        df_ret_sub_industries_last2_top.sort_values(by=['Cumulative % Return Rank'], inplace=True)

        print(df_ret_sub_industries_last2_top.to_string(index=False))

![SP500_GICS_Consumer_Staples_Sector_Sub_Industries_Top_5_Cumulative_Returns_Data_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_GICS_Consumer_Staples_Sector_Sub_Industries_Top_5_Cumulative_Returns_Data_Python.jpg?raw=true)

The **Agricultural Products & Services** Sub-Industry had the strongest Cumulative % Return in the **Consumer Staples** Sector.












        



