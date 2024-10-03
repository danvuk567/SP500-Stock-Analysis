Let's do some analysis on a portfolio of stocks. We will be adding new functions to our *custom_python_functions.py* file which can be re-used in this project. 

## Modify custom re-usable functions: *[custom_python_functions.py](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Custom-Python-Functions/custom_python_functions.py)*

Let's define a function called *calculate_portfolio_return* which will calculate returns for a portfolio of Tickers based on average log returns. The returns dataframe and period type are passed as input parameters and the returns dataframe is returned with the same columns as the *calculate_return* function.


    def calculate_portfolio_return(df_tmp, period):
    
            """
            Calculate the returns of a portfolio of Tickers using an average of cumulative returns.
    
            Parameters:
            - df_tmp: The DataFrame containing the historical data.
            - period: A string indicating the period ('Year', 'Quarter', 'Month', or 'Daily').

            Returns:
            - A DataFrame with new columns: '% Return', 'Cumulative % Return', 'Annualized % Return', 'Annualized Volatility', 
              'Annualized Downside Volatility', or None if not applicable.
            """
    
            # Assign the number of periods based on the specified period type
            if period == 'Year':
                no_of_periods = 1  # 1 year
            elif period == 'Quarter':
                no_of_periods = 4  # 4 quarters in a year
            elif period == 'Month':
                no_of_periods = 12  # 12 months in a year
            else:
                no_of_periods = 252  # Default to daily data (252 trading days in a year)
        
            if period == 'Daily':
                label = ''
            else:
                label = period + ' '

            # Drop unnecessary columns from the DataFrame to simplify calculations
            df_tmp.drop(columns=['Ticker', 'Open', 'High', 'Low', 'Close', 'Volume', label + 'Annualized % Return', label + 'Annualized Volatility', label + 'Annualized Downside Volatility'], inplace=True)

            # Calculate log returns based on cumulative percentage returns
            df_tmp['Log Return'] = np.log(1 + (df_tmp[label + 'Cumulative % Return'] / 100))

            # Calculate the average log return for each date
            df_tmp['Avg Log Return'] = df_tmp.groupby('Date')['Log Return'].transform('mean')

            # Calculate the average percentage return for each date and convert to decimal
            df_tmp['Avg % Return'] = df_tmp.groupby('Date')[label + '% Return'].transform('mean') / 100

            # Drop columns that are no longer needed after calculating averages
            df_tmp.drop(columns=['Log Return', label + '% Return', label + 'Cumulative % Return'], inplace=True)

            # Calculate cumulative percentage return from average log return
            df_tmp['Cumulative % Return'] = np.exp(df_tmp['Avg Log Return']) - 1

            # Drop the average log return column as it is no longer needed
            df_tmp.drop(columns=['Avg Log Return'], inplace=True)

            # Rename the average percentage return column to '% Return' for clarity
            df_tmp.rename(columns={'Avg % Return': '% Return'}, inplace=True)

            # Remove duplicate entries in the DataFrame
            df_tmp.drop_duplicates(inplace=True)

            # Count the number of returns in a rolling manner, starting from the first entry
            df_tmp['Rolling Return Count'] = df_tmp['% Return'].expanding(min_periods=1).count()
    
            # Calculate annualized return based on cumulative return and the number of returns
            df_tmp['Annualized % Return'] = ((1 + df_tmp['Cumulative % Return']) ** (no_of_periods / df_tmp['Rolling Return Count']) - 1)

            # Calculate annualized volatility based on the standard deviation of percentage returns
            df_tmp['Annualized Volatility'] = df_tmp['% Return'].expanding().std() * np.sqrt(no_of_periods)

            # Calculate annualized downside volatility (only for negative returns)
            df_tmp['Annualized Downside Volatility'] = df_tmp['% Return'].expanding().apply(
                lambda x: x[x < 0].std() * np.sqrt(no_of_periods) if len(x[x < 0]) > 0 else 0)

            # Drop the rolling return count column after its use
            df_tmp.drop(columns=['Rolling Return Count'], inplace=True)

            # Round the values for presentation to two decimal places
            df_tmp['% Return'] = round(df_tmp['% Return'] * 100, 2)
            df_tmp['Cumulative % Return'] = round(df_tmp['Cumulative % Return'] * 100, 2)
            df_tmp['Annualized % Return'] = round(df_tmp['Annualized % Return'] * 100, 2)
            df_tmp['Annualized Volatility'] = round(df_tmp['Annualized Volatility'] * 100, 2)
            df_tmp['Annualized Downside Volatility'] = round(df_tmp['Annualized Downside Volatility'] * 100, 2)
    
            # Rename return columns based on the specified period type, if not daily
            if period != 'Daily':
                df_tmp.rename(columns={'% Return': period + ' % Return'}, inplace=True)    
                df_tmp.rename(columns={'Cumulative % Return': period + ' Cumulative % Return'}, inplace=True)
                df_tmp.rename(columns={'Annualized % Return': period + ' Annualized % Return'}, inplace=True)
                df_tmp.rename(columns={'Annualized Volatility': period + ' Annualized Volatility'}, inplace=True)
                df_tmp.rename(columns={'Annualized Downside Volatility': period + ' Annualized Downside Volatility'}, inplace=True)
        
            return df_tmp  # Return the modified DataFrame


If we want to see how the returns are distributed for a particular Ticke, we can plot it as a **Histogram** using the matplotlib package. This function called *plot_return_histogram* will plot a histogram and calculate the number of bins based on the Freedman-Diaconis rule that uses quartile range. For more information on this rule. refer to this link: [Freedman–Diaconis rule](https://en.wikipedia.org/wiki/Freedman%E2%80%93Diaconis_rule). We can also compare how the returns measure up against all the returns that are normalized and plotted as a line representing a Normal Distribution. The scipy package would need to be imported. Another line can be drawn that can smooth the Ticker return bins using the Gaussion KDE (Kernel Density Estimation) function from the scipy package. For more informtion on this, refer to this link: [Kernel density estimation](https://en.wikipedia.org/wiki/Kernel_density_estimation). The *plot_return_histogram* function takes the return dataframe, return_type and ticker as input parameters.


    from scipy.stats import norm, gaussian_kde
    
    def plot_return_histogram(df_tmp, return_type, ticker):
    
        """
        Plot a histogram of return_type for a specific ticker with a normal distribution curve based on all tickers.
    
        Parameters:
        - df_tmp: DataFrame containing return data for all tickers.
        - return_type: Name of the column containing percentage returns.
        - ticker: Ticker symbol to filter the DataFrame.
        """
    
        # Filter rows for the specific ticker
        df_ticker = df_tmp[df_tmp['Ticker'] == ticker]
    
        # Ensure the DataFrame contains the required columns
        if return_type not in df_tmp.columns:
            raise ValueError(f"Required column '{return_type}' is missing.")
    
        # Compute global mean and standard deviation from all tickers
        all_returns = df_tmp[return_type]
        global_mean = np.mean(all_returns)
        global_std_dev = np.std(all_returns)
    
        # Compute histogram for the specific ticker
        ticker_returns = df_ticker[return_type]
    
        # Calculate the interquartile range (IQR)
        IQR = np.percentile(ticker_returns, 75) - np.percentile(ticker_returns, 25)
    
        # Calculate the bin width using the Freedman-Diaconis rule
        bin_width = 2 * IQR / np.cbrt(len(ticker_returns))
    
        # Calculate the optimal bin width using Freedman-Diaconis rule
        num_bins = int((ticker_returns.max() - ticker_returns.min()) / bin_width)
    
        plt.figure(figsize=(12, 8))
    
        # Compute histogram and keep counts (not densities)
        count, bins, _ = plt.hist(ticker_returns, bins=num_bins, alpha=0.6, density=False, edgecolor='black', label=f'Frequency for {ticker}')
        total_count = np.sum(count)
    
        # Compute KDE for a smooth line
        kde = gaussian_kde(ticker_returns, bw_method='scott')  # 'scott' method automatically chooses bandwidth
        x_kde = np.linspace(ticker_returns.min(), ticker_returns.max(), 1000)  # Generate points for smooth line
        y_kde = kde(x_kde)  # KDE values
        y_kde_normalized = y_kde * len(ticker_returns) * bin_width  # Normalize KDE to match histogram counts   
        plt.plot(x_kde, y_kde_normalized, 'g-', linewidth=2, label='KDE (Smooth Line) for ' + ticker)
    
        # Calculate bin width for scaling the normal distribution
        actual_bin_width = bins[1] - bins[0]  # Use the actual bin width from the histogram calculation
    
        # Plot the normal distribution curve based on all tickers and scale to match histogram
        x = np.linspace(min(bins), max(bins), 100)
        p = norm.pdf(x, global_mean, global_std_dev)  # PDF of the normal distribution
        p = p * total_count * actual_bin_width  # Scale PDF by total count and bin width to match frequency

        # Plot the normal distribution curve
        plt.plot(x, p, 'r-', linewidth=2, label='Normal Distribution (All Tickers)')

        # Add red dotted vertical line at x = 0
        plt.axvline(x=0, color='red', linestyle='--', linewidth=2, label='x = 0')
    
        # Set labels and title
        plt.xlabel(return_type)
        plt.ylabel('Frequency')
        plt.title(f'Frequency Histogram of {return_type} for {ticker} with Normal Distribution Curve')
    
        # Add legend and grid
        plt.legend()
        plt.grid(True)
        plt.show() 


If we want to visualize and compare various Tickers using a return type vs another measure, we can use a **Bubble Chart**. The size of the bubble is represented by the size measure. Let's create a function called *plot_returns_bubble_chart* that will display the bubble chart using plotly express scatter plots. For a large group of Tickers such as those in the S&P500, it would be hard to view a snapshot of the chart so we can tweak the code to show a legend of the top 10 Tickers based on a custom performance adjusted measure using the return type value multiplied by the size measure value. The *plot_returns_bubble_chart* function takes the return dataframe, return_type and size_type as input parameters. 


        def plot_returns_bubble_chart(df_tmp, return_type, size_type):
    
            """
            Plot a bubble chart where the x-axis is Ticker, 
            y-axis is return_type.
    
            Parameters:
            - df: DataFrame with columns 'Ticker', return_type, and other metric as size_type
            """
    
            # Filter out rows where size_type has negative or zero values
            df_tmp2 = df_tmp[df_tmp[size_type] > 0].copy()
    
            # Calculate the Performance-Adjusted Return as return_type * size_type
            df_tmp2['Performance Return'] = df_tmp2[return_type] * df_tmp2[size_type]

            # Sort by the Performance Return and get the top 10 tickers
            top_10_tickers = df_tmp2.nlargest(10, 'Performance Return')[['Ticker', 'Performance Return', return_type, size_type]]
    
            fig = px.scatter(
                df_tmp2, 
                x='Ticker',  # X-axis is Ticker
                y=return_type,  # Y-axis is return_type
                size=size_type,  # Bubble size based on size_type
                color='Ticker',  # Different colors for different tickers
                hover_name='Ticker',  # Display Ticker name on hover
                size_max=60,  # Maximum bubble size
                title=f"Bubble Chart: {return_type} by Ticker with Bubble Size as {size_type}",
            )
    
            # Customize chart appearance
            fig.update_layout(
                xaxis_title="Ticker",
                yaxis_title=return_type,
                showlegend=False,
                plot_bgcolor="lightgrey"  # Set background color
            )
    
            # Add an annotation for the top 10 tickers
            annotations = []
            for i, row in top_10_tickers.iterrows():
                # Get the corresponding y value
                y_value = df_tmp2.loc[df_tmp2['Ticker'] == row['Ticker'], return_type].values[0]
                annotations.append(
                    dict(
                        x=row['Ticker'],
                        y=y_value,
                        xref="x",
                        yref="y",
                        text=row['Ticker'],  # Show Ticker name
                        showarrow=True,
                        arrowhead=2,
                        ax=50,  # Move the annotation right
                        ay=-20,  # Adjust the vertical position of annotation
                        font=dict(size=10, color="black")
                    )
                )

            # Add the annotations to the layout
            fig.update_layout(annotations=annotations)

            # Create a separate legend box on the right for the top 10 tickers
            legend_text = '<br>'.join([f"{row['Ticker']}, {row[return_type]}, {row[size_type]}" for _, row in top_10_tickers.iterrows()])
    
            # Add a text box to display the top 10 tickers legend
            fig.add_annotation(
                dict(
                    x=1.05,  # Position the legend outside of the plot
                    y=0.5,  # Vertically center the legend
                    xref='paper', 
                    yref='paper',
                    showarrow=False,
                    text=f'<b>Top 10 Tickers by<br>{return_type}<br>and {size_type}</b><br>{legend_text}',
                    font=dict(size=12, color="black"),
                    align='left',
                    bordercolor='black',
                    borderwidth=1,
                    borderpad=5,
                    bgcolor="lightgrey"
                )
            )

            # Show the figure
            fig.show()

    
This function called *plot_period_returns_by_ticker_box_plot* creates box plots using the seaborn and matplotlib package. The % Returns are plotted by Ticker for period type. This function takes the return dataframe and period type as input parameters.

    def plot_period_returns_by_ticker_box_plot(df_ret, period):
    
        """
        Plots a box plot of returns for a given ticker and period.
    
        Parameters:
        - df_ret: DataFrame containing return data.
        - period: Time period for returns (e.g., 'Daily', 'Year', etc.).
        """
    
        # Define properties for outliers in the box plot
        # 'marker' defines the shape of the outliers
        # 'color' sets the color of the outliers
        # 'alpha' adjusts the transparency of the outliers
        # 'markersize' sets the size of the outlier markers
        flierprops = dict(marker='o', color='red', alpha=0.5, markersize=8)

        # Create a figure with a specified size for the plot
        plt.figure(figsize=(12, 8))
    
        # If the period is 'Daily', treat it as an empty string for labeling purposes
        # Otherwise, append a space after the period string for readability in the title
        period_label = '' if period == 'Daily' else f'{period} '

        # Create the boxplot, with 'Ticker' on the x-axis and returns on the y-axis
        sns.boxplot(x='Ticker', y=f'{period_label}% Return', data=df_ret, hue='Ticker', palette="Set2", flierprops=flierprops, legend=False)
        plt.title(f'{period_label}% Returns by Ticker')  
        plt.ylabel(f'{period_label}% Returns')  
        plt.xlabel('Ticker')
                      
        # Add gridlines to the y-axis for clarity, using a dashed line style and slight transparency
        plt.grid(axis='y', linestyle='--', alpha=0.7)

        # Rotate the x-axis labels by 45 degrees for better readability, especially if there are many years
        plt.xticks(rotation=45)
    
        # Display the plot
        plt.show()

If we want to see how the returns are correlated, we can use the Pearson correlation coefficient. For more information on this, refer to this link: [The Correlation Coefficient: What It Is and What It Tells Investors](https://www.investopedia.com/terms/c/correlationcoefficient.asp). We start by creating a **Pivot Table** to group the return values under Ticker columns. We can use the pandas dataframe built-in function *corr()* on the pivot table to retrieve the correlation matrix. To plot the correlation matrix, we can create a **Heatmap** using the seaborn package. This function takes the return dataframe and return type as input parameters.


        def plot_ticker_correlations(df_tmp, return_type):
    
            """
            Compute and visualize the correlation between the returns of different tickers.
    
            Parameters:
            - df_tmp: DataFrame containing return data for multiple tickers.
            - return_type: Column name containing the returns to be correlated.

    
            Returns:
            - Correlation matrix and heatmap.
            """
    
            # Pivot the DataFrame to have tickers as columns and dates as index
            df_pivot = df_tmp.pivot_table(index='Date', columns='Ticker', values=return_type)
    
            # Calculate the correlation matrix
            corr_matrix = df_pivot.corr()
    
            # Plot the heatmap of the correlation matrix
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0,
                        cbar_kws={'label': 'Correlation'}, linewidths=0.5)
    
            plt.title('Correlation between Tickers based on {return_Type}')
            plt.show()
    
            return corr_matrix


## Portfolio Performance Analysis: *[Portfolio-Performance-Analysis.ipynb](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Python-Portfolio-Performance-Analysis/Portfolio-Performance-Analysis.ipynb)*

Let's go ahead and analyze a basket of stocks from the S&P 500 as an investment portfolio. We will import the necessary packages, connect to the database, query the database for our pricing data bind it to the         df_pricing dataframe. Before we proceed any futher, we want to focus on stocks that existed from the start of the 4 year data we stored so that any aggregated return comparison is not skewed by newer stocks that         were traded later on.

        # Determine the first date for each ticker
        first_dates = df_pricing.groupby('Ticker')['Date'].min().reset_index()
        first_dates.rename(columns={'Date': 'First Date'}, inplace=True)

        # Count how many tickers share the same first date
        count_first_dates = first_dates['First Date'].value_counts().reset_index()
        count_first_dates.columns = ['First Date', 'Count']

        # Filter for first dates that occur more than once and take the min date
        valid_first_dates = count_first_dates[count_first_dates['Count'] > 1]['First Date']
        min_valid_first_date = valid_first_dates.min()

        # Merge back to keep only those tickers with the same first date
        df_pricing_filtered = df_pricing.merge(first_dates, on='Ticker', suffixes=('', '_y'))  # Specify suffixes here
        df_pricing_filtered = df_pricing_filtered[df_pricing_filtered['First Date'].isin([min_valid_first_date])].copy()

        df_pricing_filtered.drop(columns=['First Date'], inplace=True)
    
        if 'First Date_y' in df_pricing_filtered.columns:
            df_pricing_filtered.drop(columns=['First Date_y'], inplace=True)
    
        df_pricing_filtered.sort_values(by=['Ticker', 'Date'], inplace=True)

        # Show count of original Tickers
        ticker_cnt = len(df_pricing['Ticker'].unique())
        ticker_cnt2 = len(df_pricing_filtered['Ticker'].unique())
        print(f'Original Ticker list count: {ticker_cnt}')
        print(f'Filtered Ticker list count: {ticker_cnt2}')

We originally had **503** Tickers and now we have **496** Tickers that we will work with to create a portfolio.    

Let's say we want to determine what the top 10 stocks are for the 1st 2 years based on Annualize Sortino Retio. First, We can do this calculating the returns, using a risk free rate of 1.5 which is roughly average at the time and then ranking the top 10.

        two_years_after_min_date = min_valid_first_date + pd.DateOffset(days=(365)*2)
        two_years_after_min_date_str = two_years_after_min_date.strftime('%Y-%m-%d')

        period_label = 'Daily'
        date_filter = (df_pricing_filtered['Date'] < two_years_after_min_date_str)
        df_pricing_second_year = df_pricing_filtered.loc[date_filter].copy()  # Adding .copy() here to avoid the warning
        df_pricing_second_year.sort_values(by=['Ticker', 'Date'], inplace=True)
        df_ret_second_year = calculate_return(df_pricing_second_year.copy(), 'Daily')
        df_ret_second_year.sort_values(by=['Ticker', 'Date'], inplace=True)

        df_ret_second_year_last = df_ret_second_year.copy().groupby('Ticker').tail(1)

        risk_free_rate = 1.5
        df_ret_second_year_last['Annualized Sortino Ratio'] = np.where(
            df_ret_second_year_last['Annualized Volatility'] == 0, 
            0, 
            round((df_ret_second_year_last['Annualized % Return'] - risk_free_rate) / df_ret_second_year_last['Annualized Downside Volatility'], 2)
        )

        df_ret_second_year_last['Annualized Sortino Ratio Rank'] = df_ret_second_year_last.groupby('Date')['Annualized Sortino Ratio'].rank(ascending=False).astype(int)
        num_of_ranks = 10
        df_ret_second_year_last_top = df_ret_second_year_last[df_ret_second_year_last['Annualized Sortino Ratio Rank'] <= num_of_ranks].copy()

Then we'll extract the 1st 2 year returns for the 10 as our portfolio, calculate the portfolio returns and assign a Ticker label as **PFL** to our portfolio returns.

        portfolio_tickers = df_ret_second_year_last_top['Ticker'].unique()
        print(portfolio_tickers)

        df_portfolio_tickers_ret_second_year = df_ret_second_year[df_ret_second_year['Ticker'].isin(portfolio_tickers)].copy()
        ticker_cnt = len(df_portfolio_tickers_ret_second_year['Ticker'].unique())
        print(f'Portfolio list count: {ticker_cnt}')

        df_portfolio_ret_second_year = calculate_portfolio_return(df_portfolio_tickers_ret_second_year.copy(), 'Daily')
        df_portfolio_ret_second_year['Ticker'] = 'PFL'
        df_portfolio_ret_second_year.sort_values(by=['Date'], inplace=True)

We'll combine the returns of the top 10 and the portfolio and then plot the top 10 tickers and the portfolio cumulative returns in a line chart.

        df_ret_second_year_comb = pd.concat([df_portfolio_tickers_ret_second_year, df_portfolio_ret_second_year], axis=0)
        df_ret_second_year_comb.sort_values(by=['Ticker','Date'], inplace=True)
        plot_returns_line_chart(df_ret_second_year_comb, 'Daily', 'Cumulative % Return')

![SP500_Portfolio_Cumulative_Returns_Line_Chart_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Portfolio_Cumulative_Returns_Line_Chart_Python.jpg?raw=true)



###########################################################################################################################################################




        

Next we extract the daily return dataframe as *df_portfolio_pricing* for the 10 Tickers that had the highest Calmar Ratio from our prior Equity perfromance analysis. Of course, we are choosing these Tickers in hindsight and there is no way to know for sure which basket of stocks would have given the highest Calmar Ratio 3 years ago. This portfolio will simply demonstrate what can be observed from a good risk-adjusted performing portfolio.

        portfolio_tickers= ['LLY','SMCI','TRGP','MCK','MRO','PWR','MPC','XOM','FANG','IRM']
        df_portfolio_pricing = df_pricing_filtered[df_pricing_filtered['Ticker'].isin(portfolio_tickers)].copy()
        ticker_cnt3 = len(df_portfolio_pricing['Ticker'].unique())
        print(f'Portfolio list count: {ticker_cnt3}')

If we want to compare the returns of the S&P 500 Tickers to our portfolio, one way to do this is to use an average return for our portfolio. We will calculate the daily returns as *df_ret* and calculate the average returns for our portfolio as *df_portfolio_ret*. We'll assign the Ticker label for our portfolio as **'PFL'**.

        df_ret = calculate_return(df_pricing_filtered.copy(), 'Daily')
        df_ret.drop(columns=['Open', 'High', 'Low', 'Close', 'Volume'], inplace=True)
        df_ret.sort_values(by=['Ticker', 'Date'], inplace=True)

Let's observe our portfolio returns in Histogram and compare it the Normalized Distribution of all the S&P 500 returns. We can combine our portfolio returns with all daily returns and then call our custom function *plot_return_histogram* to create the chart.

        df_ret_comb = pd.concat([df_ret, df_portfolio_ret], axis=0)
        df_ret_comb.sort_values(by=['Ticker','Date'], inplace=True)
        plot_return_histogram(df_ret_comb, '% Return', 'PFL')

 ![SP500_Portfolio_Histogram_Chart_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Portfolio_Histogram_Chart_Python.jpg?raw=true)

We can see that portfolio returns are more positively skewed than the S&P 500 returns. The frequency of negative returns tend to be less than the S&P 500 negative returns for those returns that are < 1.5%. The portfolio also tends to have a higher frequency of returns for those returns between 0% and 2%. Although, the portfolio also tends to have a slightly lower frequency of returns for those returns that are > 2.0%.

Let's go ahead and calculate the *'Max Drawdown'*, *'Annualized Sharpe Ratio'*, *'Annualized Sortino Ratio'*, and *'Calmar Ratio'* for all the returns in df_ret_comb.

        last_dates = df_ret_comb['Date'].max()
        three_years_ago = last_dates - pd.DateOffset(days=252 * 3)
        three_years_ago_str = three_years_ago.strftime('%Y-%m-%d')

        period_label = 'Daily'
        date_filter = (df_ret_comb['Date'] >= three_years_ago_str)
        df_ret_comb_filter = df_ret_comb.loc[date_filter].copy()  # Adding .copy() here to avoid the warning
        df_ret_comb_filter = calculate_drawdowns(df_ret_comb_filter, period_label)
        df_ret_comb_last = df_ret_comb_filter.copy().groupby('Ticker').tail(1)
        df_ret_comb_last.sort_values(by=['Ticker'], ascending=True, inplace=True)

        risk_free_rate = 2.5
        df_ret_comb_last['Annualized Sharpe Ratio'] = np.where(
            df_ret_comb_last['Annualized Volatility'] == 0, 
            0, 
            round((df_ret_comb_last['Annualized % Return'] - risk_free_rate) / df_ret_comb_last['Annualized Volatility'], 2)
        )
        df_ret_comb_last['Annualized Sortino Ratio'] = np.where(
            df_ret_comb_last['Annualized Volatility'] == 0, 
            0, 
            round((df_ret_comb_last['Annualized % Return'] - risk_free_rate) / df_ret_comb_last['Annualized Downside Volatility'], 2)
        )
        df_ret_comb_last['Calmar Ratio'] = np.where(
            df_ret_comb_last['Max % Drawdown'] == 0, 
            0, 
            round(df_ret_comb_last['Annualized % Return'] / df_ret_comb_last['Max % Drawdown'], 2)
        )
        df_ret_comb_last.sort_values(by=['Ticker'], ascending=True, inplace=True)


We'll also create a bubble chart to show the Annualized % Return as a bubble with Annualized Sortino Ratio as the bubble size. We'll highlight the top 10 tickers based on the top values.

![SP500_Portfolio_Annualized_Sortino_Ratio_Bubble_Chart_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Portfolio_Annualized_Sortino_Ratio_Bubble_Chart_Python.jpg?raw=true)

Our portfolio, **PFL** also came in 2nd with 2nd highest **Annualized % Return** of **57.63%** and highest **Annualized Sortino Ratio** of **3.52**. This emphasizes that the portfolio is optimum in terms of risk vs. reward as opposed to other stocks.









        
