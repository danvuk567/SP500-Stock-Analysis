# Python Portfolio Performance Analysis

Let's do some analysis on a portfolio of stocks. We will be adding new functions to our *custom_python_functions.py* file which can be re-used in this project. 

## Modify custom re-usable functions: *[custom_python_functions.py](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Custom-Python-Functions/custom_python_functions.py)*

Let's define a function called *calculate_portfolio_return* which will calculate returns for a portfolio of security class type based on average log returns. We will need to drop the security class list to aggregate all the returns by date. The returns dataframe, a security class list, and period type are passed as input parameters and the returns dataframe is returned with the same columns as the *calculate_return* function.


    def calculate_portfolio_return(df_tmp, security_class_list, period):
    
            """
            Calculate the returns of a portfolio of Tickers using an average of cumulative returns.
    
            Args:
                - df_tmp: The DataFrame containing the historical data.
                - security_class_list: A list of strings representing the security class type columns ('Sector', 'Industry Group', 'Industry', 
                'Sub_Industry', 'Ticker').
                - period: A string representing the period type column ('Year', 'Quarter', 'Month', or 'Daily').

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
            columns_to_drop = security_class_list + ['Open', 'High', 'Low', 'Close', 'Volume', 
                                              label + 'Annualized % Return', label + 'Annualized Volatility', 
                                              label + 'Annualized Downside Volatility']
    
            # Keep only those columns that exist in df_tmp
            columns_to_drop = [col for col in columns_to_drop if col in df_tmp.columns]

            df_tmp.drop(columns=columns_to_drop, inplace=True)

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


If we want to see how the returns are distributed for a particular Ticker, we can plot it as a **Histogram** using the **matplotlib** package. This function called *plot_return_histogram* will plot a Histogram and calculate the number of bins based on the **Freedman-Diaconis rule** that uses quartile range. For more information on this rule. refer to this link: [Freedman–Diaconis rule](https://en.wikipedia.org/wiki/Freedman%E2%80%93Diaconis_rule). We can also compare how the returns measure up against all the returns that are normalized and plotted as a line representing a **Normal Distribution**. The **scipy** package would need to be imported. Another line can be drawn that can smooth the Ticker return bins using the **Gaussion KDE (Kernel Density Estimation) function** from the scipy package. For more informtion on this, refer to this link: [Kernel density estimation](https://en.wikipedia.org/wiki/Kernel_density_estimation). The *plot_return_histogram* function takes the return dataframe, return type and security class type value as input parameters.


    from scipy.stats import norm, gaussian_kde
    
     def plot_return_histogram(df_tmp, return_type, security_class, security_class_val):
    
        """
        Plot a histogram of '% Return' for a specific security class type value with a normal distribution curve based on all security class 
        type values.
    
        Args::
            - df_tmp: DataFrame containing return data for all security class type values.
            - return_type: String representing the name of the column containing returns.
            - security_class: A string representing the security class type column ('Sector', 'Industry Group', 'Industry', 'Sub_Industry', 
            'Ticker').
            - security_class_val: A string representing the value for security class type column ('Sector', 'Industry Group', 'Industry',  
            'Sub_Industry', 'Ticker').
        """
    
        # Filter rows for the specific security class value
        df_security_class = df_tmp[df_tmp[security_class] == security_class_val]
    
        # Ensure the DataFrame contains the required columns
        if return_type not in df_tmp.columns:
            raise ValueError(f"Required column '{return_type}' is missing.")
    
        # Compute global mean and standard deviation from all tickers
        all_returns = df_tmp[return_type]
        global_mean = np.mean(all_returns)
        global_std_dev = np.std(all_returns)
    
        # Compute histogram for the specific security class value
        security_class_returns = df_security_class[return_type]
    
        # Calculate the interquartile range (IQR)
        IQR = np.percentile(security_class_returns, 75) - np.percentile(security_class_returns, 25)
    
        # Calculate the bin width using the Freedman-Diaconis rule
        bin_width = 2 * IQR / np.cbrt(len(security_class_returns))
    
        # Calculate the optimal bin width using Freedman-Diaconis rule
        num_bins = int((security_class_returns.max() - security_class_returns.min()) / bin_width)
    
        plt.figure(figsize=(12, 8))
    
        # Compute histogram and keep counts (not densities)
        count, bins, _ = plt.hist(security_class_returns, bins=num_bins, alpha=0.6, density=False, edgecolor='black', label=f'Frequency for {security_class_val}')
        total_count = np.sum(count)
    
        # Compute KDE for a smooth line
        kde = gaussian_kde(security_class_returns, bw_method='scott')  # 'scott' method automatically chooses bandwidth
        x_kde = np.linspace(security_class_returns.min(), security_class_returns.max(), 1000)  # Generate points for smooth line
        y_kde = kde(x_kde)  # KDE values
        y_kde_normalized = y_kde * len(security_class_returns) * bin_width  # Normalize KDE to match histogram counts   
        plt.plot(x_kde, y_kde_normalized, 'g-', linewidth=2, label=f'KDE (Smooth Line) for {security_class_val}')
    
        # Calculate bin width for scaling the normal distribution
        actual_bin_width = bins[1] - bins[0]  # Use the actual bin width from the histogram calculation
    
        # Plot the normal distribution curve based on all security class type values and scale to match histogram
        x = np.linspace(min(bins), max(bins), 100)
        p = norm.pdf(x, global_mean, global_std_dev)  # PDF of the normal distribution
        p = p * total_count * actual_bin_width  # Scale PDF by total count and bin width to match frequency

        # Plot the normal distribution curve
        plt.plot(x, p, 'r-', linewidth=2, label=f'Normal Distribution for all values of {security_class}')
    
        # Add red dotted vertical line at x = 0
        plt.axvline(x=0, color='red', linestyle='--', linewidth=2, label='x = 0')
    
        # Set labels and title
        plt.xlabel(return_type)
        plt.ylabel('Frequency')
        plt.title(f'Frequency Histogram of {return_type} for {security_class_val} with Normal Distribution Curve')
    
        # Add legend and grid
        plt.legend()
        plt.grid(True)
        plt.show()    


If we want to visualize and compare various Tickers using a return type vs another measure, we can use a **Bubble Chart**. The size of the bubble is represented by the size measure. Let's create a function called *plot_returns_bubble_chart* that will display the Bubble Chart using plotly express scatter plots. For a large group of Tickers such as those in the S&P500, it would be hard to view a snapshot of the chart so we can tweak the code to show a legend highlighting the top 10 Tickers based on a custom performance adjusted measure as *size_type*. The *plot_returns_bubble_chart* function takes the return dataframe, return type, size type, security class type as input paramters. It also takes True or False for displaying top N values in the legend along with N as input parameters.


        def plot_returns_bubble_chart(df_tmp, return_type, size_type, security_class, is_top, top_val):
    
            """
            Plot a bubble chart where the x-axis is the security class type value, 
            y-axis is return_type.
    
            Args:
                - df_tmp: DataFrame with columns security class, return_type, and other metric as size_type.
                - return_type: String representing the name of the column containing returns.
                - size_type: String representing the name of the the column containing the bubble size values.
                - security_class: A string representing the security class type column ('Sector', 'Industry Group', 
                  'Industry', 'Sub_Industry', 'Ticker').
                - security_class_val: A string representing the value of the security class type column ('Sector', 'Industry Group', 
                  'Industry', 'Sub_Industry', 'Ticker').
                - is_top: Boolean value indicating whether we want to show top vlaues in the legend.
                - top_val: Integer representing N for top N values.      
            """
    
            # Filter out rows where size_type has negative or zero values
            df_tmp2 = df_tmp[df_tmp[size_type] > 0].copy()
   
            if is_top:
                # Sort by the size_type and get the top top_val security class type values
                top_security_classes = df_tmp2.nlargest(top_val, size_type)[[security_class, return_type, size_type]]
            else:
                top_security_classes = df_tmp2[[security_class, return_type, size_type]]
    
            fig = px.scatter(
                df_tmp2, 
                x=security_class,  # X-axis is security class type value
                y=return_type,  # Y-axis is return_type
                size=size_type,  # Bubble size based on size_type
                color=security_class,  # Different colors for different security class type values
                hover_name=security_class,  # Display security class type value on hover
                size_max=60,  # Maximum bubble size
                title=f"Bubble Chart: {return_type} by {security_class} with Bubble Size as {size_type}",
            )
    
            # Customize chart appearance
            fig.update_layout(
                xaxis_title=security_class,
                yaxis_title=return_type,
                showlegend=False,
                plot_bgcolor="lightgrey"  # Set background color
            )
    
            # Add an annotation for the top 10 tickers
            annotations = []
            for i, row in top_security_classes.iterrows():
                # Get the corresponding y value
                y_value = df_tmp2.loc[df_tmp2[security_class] == row[security_class], return_type].values[0]
                annotations.append(
                    dict(
                        x=row[security_class],
                        y=y_value,
                        xref="x",
                        yref="y",
                        text=row[security_class],  # Show security name
                        showarrow=True,
                        arrowhead=2,
                        ax=50,  # Move the annotation right
                        ay=-20,  # Adjust the vertical position of annotation
                        font=dict(size=10, color="black")
                    )
                )

            # Add the annotations to the layout
            fig.update_layout(annotations=annotations)

            if is_top:
                # Create a separate legend box on the right for the top top_val security class type
                legend_text = '<br>'.join([f"{row[security_class]}, {row[size_type]}" for _, row in top_security_classes.iterrows()])
    
                # Add a text box to display the top 10 tickers legend
                fig.add_annotation(
                    dict(
                        x=1.05,  # Position the legend outside of the plot
                        y=0.5,  # Vertically center the legend
                        xref='paper', 
                        yref='paper',
                        showarrow=False,
                        text=f'<b>Top {top_val} for {security_class} by<br>{size_type}</b><br>{legend_text}',
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

    
This function called *plot_period_returns_by_ticker_box_plot* creates **Box Plots** using the **seaborn** and **matplotlib** package. The % Returns are plotted by security class type. This function takes the return dataframe, period type and security class type as input parameters.

        def plot_period_returns_by_security_class_box_plot(df_tmp, period, security_class):
    
            """
            Plots a box plot of returns for a given security class type and period.
    
            Args:
                - df_tmp: DataFrame containing return data.
                - period: A string representing the period type column ('Year', 'Quarter', 'Month', or 'Daily').
                - security_class: A string representing the security class type column ('Sector', 'Industry Group', 
                  'Industry', 'Sub_Industry', 'Ticker').
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

            # Create the boxplot, with security class type on the x-axis and returns on the y-axis
            sns.boxplot(x=security_class, y=f'{period_label}% Return', data=df_tmp, hue=security_class, palette="Set2", flierprops=flierprops, legend=False)
            plt.title(f'{period_label}% Returns by {security_class}')  
            plt.ylabel(f'{period_label}% Returns')  
            plt.xlabel(security_class)
                      
            # Add gridlines to the y-axis for clarity, using a dashed line style and slight transparency
            plt.grid(axis='y', linestyle='--', alpha=0.7)

            # Rotate the x-axis labels by 45 degrees for better readability, especially if there are many years
            plt.xticks(rotation=45)
    
            # Display the plot
            plt.show()

This function called *calculate_information_ratio* calculates the ***Information Ratio*** which measures how consistently a portfolio outperforms its benchmark with respect to magnitude of risk taken. ***Information Ratio = (Portfolio Return − Benchmark Return) / Tracking Error, where Tracking Error = Standard deviation of difference between Portfolio and Benchmark returns***. For more information on the Information Ratio, refer to this link: [Information Ratio (IR): Definition, Formula, vs. Sharpe Ratio](https://www.investopedia.com/terms/i/informationratio.asp). We can measure the excess return of the portfolio vs. the benchmark using the slopes of the respective **Regression Lines**. We will need to install the **sklearn** package if it has not been installed and import the *LinearRegression* module from sklearn. Let's define a function called *calculate_information_ratio* which requires the return datafarame, security class type, the 1st security class type value, and the 2nd security class value as the benchmark. The Information Ratio value is returned.

        from sklearn.linear_model import LinearRegression
        
        def calculate_information_ratio(df_tmp, security_class, security_class_val1, security_class_val2):
    
            """
            Compute Information Ratio of a security class type value vs. another benchmark security class type value. 
    
            Args:
                - df_tmp: DataFrame containing return data for multiple security class types.
                - security_class: A string representing the name of the the columns containing security class type ('Sector', 'Industry Group',  
                  'Industry', 'Sub_Industry', 'Ticker').
                - security_class_val1: A string representing the value of the security class type column ('Sector', 'Industry Group', 
                  'Industry', 'Sub_Industry', 'Ticker').
                - security_class_val2: A string representing the benchmark value of the security class type column ('Sector', 'Industry Group', 
                  'Industry', 'Sub_Industry', 'Ticker').  

            Returns:
                - Information Ratio value.
            """

            df_pivot = df_tmp.pivot(index='Date', columns=security_class, values='% Return')

            # Prepare the independent variable (X) for both portfolio and benchmark
            X = np.arange(len(df_pivot)).reshape(-1, 1)  # Time indices as the independent variable

            # Fit linear regression for portfolio
            model_security_class1 = LinearRegression()
            model_security_class1.fit(X, df_pivot[security_class_val1])
            slope_security_class1 = model_security_class1.coef_[0]

            # Fit linear regression for benchmark
            model_security_class2 = LinearRegression()
            model_security_class2.fit(X, df_pivot[security_class_val2])
            slope_security_class2 = model_security_class2.coef_[0]

            # Calculate excess return
            excess_return = slope_security_class1 - slope_security_class2

            # Calculate tracking error (standard deviation of the difference in returns)
            df_pivot['Excess % Return'] = df_pivot[security_class_val1] - df_pivot[security_class_val2]
            tracking_error = df_pivot['Excess % Return'].std()

            # Calculate Information Ratio
            information_ratio = round(excess_return / tracking_error, 2)

            return information_ratio

If we want to see how the returns are correlated, we can use the **Pearson correlation coefficient**. For more information on this, refer to this link: [The Correlation Coefficient: What It Is and What It Tells Investors](https://www.investopedia.com/terms/c/correlationcoefficient.asp). We start by creating a **Pivot Table** to group the return values under security class type value columns. We can use the pandas dataframe built-in function *corr()* on the pivot table to retrieve the correlation matrix. To plot the correlation matrix, we can create a **Heatmap** using the seaborn package. This function takes the return dataframe, return type and security class type as input parameters and returns the correlation matrix.


        def plot_security_class_correlations(df_tmp, return_type, security_class):
    
            """
            Compute and visualize the correlation between the returns of different tickers.
    
            Args:
                - df_tmp: DataFrame containing return data for multiple security class types.
                - return_type: A string representing the column name containing the returns to be correlated.
                - security_class: A string representing the name of the the columns containing security class type ('Sector', 'Industry Group',  
                'Industry', 'Sub_Industry', 'Ticker').

            Returns:
                - Correlation matrix.
            """
    
            # Pivot the DataFrame to have security class types as columns and dates as index
            df_pivot = df_tmp.pivot_table(index='Date', columns=security_class, values=return_type)
    
            # Calculate the correlation matrix
            corr_matrix = df_pivot.corr()
    
            # Plot the heatmap of the correlation matrix
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, center=0,
                        cbar_kws={'label': 'Correlation'}, linewidths=0.5)
    
            plt.title(f'Correlation between each {security_class} based on {return_type}')
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

Let's say we want to determine what the top 10 stocks are for the 1st 2 years (2021 to 2022) based on Annualize Sortino Retio. First, We can do this calculating the returns, using a risk free rate of 1.5 which is roughly average at the time and then rank the top 10.

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

Then we'll extract the 1st 2 year returns for the 10 as our portfolio, calculate the portfolio returns using our custom function *calculate_portfolio_return* that uses average Ticker log returns. We assign a Ticker label as **PFL** to our portfolio returns.

        portfolio_tickers = df_ret_second_year_last_top['Ticker'].unique()
        print(portfolio_tickers)

        df_portfolio_tickers_ret_second_year = df_ret_second_year[df_ret_second_year['Ticker'].isin(portfolio_tickers)].copy()
        ticker_cnt = len(df_portfolio_tickers_ret_second_year['Ticker'].unique())
        print(f'Portfolio list count: {ticker_cnt}')

![SP500_Portfolio_list_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Portfolio_list_Python.jpg?raw=true)

        df_portfolio_ret_second_year = calculate_portfolio_return(df_portfolio_tickers_ret_second_year.copy(), ['Ticker'], 'Daily')
        df_portfolio_ret_second_year['Ticker'] = 'PFL'
        df_portfolio_ret_second_year.sort_values(by=['Date'], inplace=True)

We'll combine the returns of the top 10 and the portfolio and then plot a **Line Chart** of the top 10 tickers using our custom function *plot_returns_line_chart* for the portfolio cumulative returns.

        df_ret_second_year_comb = pd.concat([df_portfolio_tickers_ret_second_year, df_portfolio_ret_second_year], axis=0)
        df_ret_second_year_comb.sort_values(by=['Ticker','Date'], inplace=True)
        plot_returns_line_chart(df_ret_second_year_comb, 'Daily', 'Cumulative % Return', 'Ticker')

![SP500_Portfolio_Cumulative_Returns_Line_Chart_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Portfolio_Cumulative_Returns_Line_Chart_Python.jpg?raw=true)

We can see that our portfolio **PFL** (pink line) has returns somewhere around 4th place that are smoother and less volatile than top performing stocks. This is a result of diversification that can reduce risk overall.

Now let's observe our top 10 Ticker and Portfolio Annualized Sortino Ratio values.

    df_ret_second_year_comb_last = df_ret_second_year_comb_last[['Ticker', 'Date', 'Annualized % Return', 'Annualized Sortino Ratio']]
    df_ret_second_year_comb_last.sort_values(by=['Annualized Sortino Ratio'], ascending=False, inplace=True)

    print(df_ret_second_year_comb_last.to_string(index=False))

![SP500_Portfolio_Annualized_Sortino_Ratio_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Portfolio_Annualized_Sortino_Ratio_Python.jpg?raw=true)

We can see that **MCK** had the highest Annualized Sortino Ratio of **3.07** and that our Portfolio **PFL** had the 2nd highest at **3.04**. We can also plot and compare the Annualized Sortino Ratio for all Tickers and the portfolio in a **Bubble Chart** using our custom function *plot_returns_bubble_chart* with the following code.

    df_ret_second_year_comb2 = pd.concat([df_ret_second_year_last, df_portfolio_ret_second_year], axis=0)
    df_ret_second_year_comb2.sort_values(by=['Ticker','Date'], inplace=True)

    df_ret_second_year_comb2_last = df_ret_second_year_comb2.copy().groupby('Ticker').tail(1)

    risk_free_rate = 1.5
    df_ret_second_year_comb2_last['Annualized Sortino Ratio'] = np.where(
        df_ret_second_year_comb2_last['Annualized Volatility'] == 0, 
        0, 
        round((df_ret_second_year_comb2_last['Annualized % Return'] - risk_free_rate) / df_ret_second_year_comb2_last['Annualized Downside Volatility'], 2)
    )
    df_ret_second_year_comb2_last.sort_values(by=['Ticker'], ascending=True, inplace=True)

    plot_returns_bubble_chart(df_ret_second_year_comb2_last, 'Annualized % Return', 'Annualized Sortino Ratio', 'Ticker', True, 10)

![SP500_Portfolio_Annualized_Sortino_Ratio_Bubble_Chart_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Portfolio_Annualized_Sortino_Ratio_Bubble_Chart_Python.jpg?raw=true)

What would happen if we invested in the top 10 Annualized Sortino Ratio Tickers at the start of 2023? Would the portfolio still be in the Annualized Sortino Ratio top 10?

    date_filter2 = (df_pricing_filtered['Date'] >= two_years_after_min_date_str)
    df_pricing_after_second_year = df_pricing_filtered.loc[date_filter2].copy()  # Adding .copy() here to avoid the warning

    df_ret_after_second_year = calculate_return(df_pricing_after_second_year.copy(), 'Daily')
    df_portfolio_tickers_ret_after_second_year = df_ret_after_second_year[df_ret_after_second_year['Ticker'].isin(portfolio_tickers)].copy()

    df_portfolio_ret_after_second_year = calculate_portfolio_return(df_portfolio_tickers_ret_after_second_year.copy(), ['Ticker'], 'Daily')
    df_portfolio_ret_after_second_year['Ticker'] = 'PFL'
    df_portfolio_ret_after_second_year.sort_values(by=['Date'], inplace=True)

    df_ret_after_second_year_comb = pd.concat([df_ret_after_second_year, df_portfolio_ret_after_second_year], axis=0)
    df_ret_after_second_year_comb.sort_values(by=['Ticker','Date'], inplace=True)

    df_ret_after_second_year_comb_last = df_ret_after_second_year_comb.copy().groupby('Ticker').tail(1)
    df_ret_after_second_year_comb_last.sort_values(by=['Ticker'], ascending=True, inplace=True)

    risk_free_rate = 2.5
    df_ret_after_second_year_comb_last['Annualized Sortino Ratio'] = np.where(
        df_ret_after_second_year_comb_last['Annualized Volatility'] == 0, 
        0, 
        round((df_ret_after_second_year_comb_last['Annualized % Return'] - risk_free_rate) / df_ret_after_second_year_comb_last['Annualized Downside Volatility'], 2)
    )
    df_ret_after_second_year_comb_last.sort_values(by=['Ticker'], ascending=True, inplace=True)

    df_ret_after_second_year_comb_last['Annualized Sortino Ratio Rank'] = df_ret_after_second_year_comb_last.groupby('Date')['Annualized Sortino Ratio'].rank(ascending=False).astype(int)
    df_ret_after_second_year_comb_last = df_ret_after_second_year_comb_last[['Ticker', 'Date', 'Annualized % Return', 'Annualized Sortino Ratio', 'Annualized Sortino Ratio Rank']]
    df_ret_after_second_year_comb_last.sort_values(by=['Annualized Sortino Ratio Rank'], ascending=True, inplace=True)

    num_of_ranks = 10
    df_ret_after_second_year_comb_last_top = df_ret_after_second_year_comb_last[df_ret_after_second_year_comb_last['Annualized Sortino Ratio Rank'] <= num_of_ranks].copy()
    df_ret_after_second_year_comb_last_top = df_ret_after_second_year_comb_last_top[['Ticker', 'Date', 'Annualized Sortino Ratio', 'Annualized Sortino Ratio Rank']]
    df_ret_after_second_year_comb_last_top.sort_values(by=['Annualized Sortino Ratio Rank'], inplace=True)

    print(df_ret_after_second_year_comb_last_top.to_string(index=False))

![SP500_Portfolio_Annualized_Sortino_Ratio_Python2.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Portfolio_Annualized_Sortino_Ratio_Python2.jpg?raw=true)

It turns out that our portfolio is not in the top 10 Annualized Sortino Ratio for the past 2 year returns.

After using percentile ranking logic, we determined that in fact, our portfolio was in the 70th percentile which is not bad but not ideal.

    df_ret_after_second_year_comb_last['Annualized Sortino Ratio Percentile Rank'] = round((1.00 - df_ret_after_second_year_comb_last.groupby('Date')['Annualized Sortino Ratio'].rank(pct=True, ascending=False)) * 100,        0).astype(int)
    df_ret_after_second_year_comb_last = df_ret_after_second_year_comb_last[['Ticker', 'Date', 'Annualized % Return', 'Annualized Sortino Ratio', 'Annualized Sortino Ratio Percentile Rank']]
    df_ret_after_second_year_comb_last.sort_values(by=['Annualized Sortino Ratio Percentile Rank'], ascending=False, inplace=True)

    df_ret_after_second_year_comb_last_ticker = df_ret_after_second_year_comb_last[df_ret_after_second_year_comb_last['Ticker'] == 'PFL'].copy()

    print(df_ret_after_second_year_comb_last_ticker.to_string(index=False))
    
![SP500_Portfolio_Annualized_Sortino_Ratio_Python3.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Portfolio_Annualized_Sortino_Ratio_Python3.jpg?raw=true)

Let's use a **Histogram** plot using our custom function *plot_return_histogram* to view our portfolio simple returns compared to all the S&P 500 Ticker simple returns.

    plot_return_histogram(df_ret_after_second_year_comb, '% Return', 'Ticker', 'PFL')

![SP500_Portfolio_Histogram_Chart_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Portfolio_Histogram_Chart_Python.jpg?raw=true)

Our portfolio **PFL** has a shape that is more narrow and longer with less fatter tails than the normal distribution of the S&P 500 Tickers. The portfolio has a higher frequency of small negative returns between 0% and -1% but also has a higher frequency of small positive returns of 0% to 1.5%.

Another way to view our portfolio returns compared to the broader market is to use a benchmark. We can calculate the returns for all Tickers as a portfolio and define it as the benchmark labelled **BM**. We then plot the Portfolio **PFL** and benchmark **BM** Cumulative % Returns in a **Line Chart** using our custom function *plot_returns_line_chart*.

    df_bench_ret_after_second_year = calculate_portfolio_return(df_ret_after_second_year.copy(), ['Ticker'], 'Daily')
    df_bench_ret_after_second_year['Ticker'] = 'BM'
    df_bench_ret_after_second_year.sort_values(by=['Date'], inplace=True)
    
    df_ret_after_second_year_comb2 = pd.concat([df_bench_ret_after_second_year, df_portfolio_ret_after_second_year], axis=0)
    df_ret_after_second_year_comb2.sort_values(by=['Ticker','Date'], inplace=True)
    plot_returns_line_chart(df_ret_after_second_year_comb2, 'Daily', 'Cumulative % Return', 'Ticker')

![SP500_Portfolio_Benchmark_Cumulative_Returns_Line_Chart_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Portfolio_Benchmark_Cumulative_Returns_Line_Chart_Python.jpg?raw=true)

We see that our portfolio is outperforming the S&P 500 basket of Tickers at certain periods which explains our slight positive skew in our Histogram chart. By end of 2024, the S&P 500 basket of Tickers has almost caught up to the portfolio.

Looking at a **Box Plot** using our custom function *plot_period_returns_by_ticker_box_plot*, we see that the portfoilo returns have more variance and outliers than the benchmark.

    plot_period_returns_by_security_class_box_plot(df_ret_after_second_year_comb2, 'Daily', 'Ticker')
    
![SP500_Portfolio_Benchmark_Returns_Box_Chart_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Portfolio_Benchmark_Returns_Box_Chart_Python.jpg?raw=true)

From the persepctive of risk vs. return alpha for our portfolio vs. the broader market, we can calculate the **Information Ratio** using our custom function *calculate_information_ratio*.

    information_ratio = calculate_information_ratio(df_ret_after_second_year_comb2, 'Ticker', 'PFL', 'BM')
    print(f'Information Ratio: {information_ratio}')

We get **Information Ratio: -0.0** which means there is no real alpha and confirms a lot of the observations we have made from the last **Line Chart** and the **Box Plot**.

Finally, let's explore the monthly smple returns for our portfolio and look at the correlations of each Ticker. We'll use our custom function *plot_ticker_correlations* to plot the **Correlation Matrix**.

    df_pricing_mth = get_pricing_data(df_pricing_filtered.copy(), 'Month')
    date_filter3 = (df_pricing_mth['Date'] >= two_years_after_min_date_str)
    df_pricing_mth_after_second_year = df_pricing_mth.loc[date_filter3].copy()

    df_ret_mth_after_second_year = calculate_return(df_pricing_mth_after_second_year.copy(), 'Month')
    df_ret_mth_after_second_year.sort_values(by=['Ticker', 'Date'], inplace=True)
    
    df_portfolio_tickers_ret_mth_after_second_year = df_ret_mth_after_second_year[df_ret_mth_after_second_year['Ticker'].isin(portfolio_tickers)].copy()
    df_corr = plot_security_class_correlations(df_portfolio_tickers_ret_mth_after_second_year, 'Month % Return', 'Ticker')

![SP500_Portfolio_Correlation_Matrix_Python.jpg](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/images/SP500_Portfolio_Correlation_Matrix_Python.jpg?raw=true)

Stocks that have correlation > 0.5 have moderate to high correlation and move together more closely. Observing our correlation matrix, we see that **LLY** and **MCK** are the only stocks that do not have moderate to high correlation with any other stocks in the portfolio. **DVN**, **MRO**, **OXY**, and **XOM** have moderate to high correlation with at least 5 out of the 10 stocks. Replacing **DVN**, **MRO**, **OXY**, and **XOM** with some other 4 stocks that are not as correlated may have produced better risk-adjusted monthly returns.

