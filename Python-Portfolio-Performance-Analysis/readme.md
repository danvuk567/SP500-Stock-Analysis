Let's do some analysis on a portfolio of stocks. We will be adding new functions to our *custom_python_functions.py* file which can be re-used in this project. 

## Modify custom re-usable functions: *[custom_python_functions.py](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Custom-Python-Functions/custom_python_functions.py)*

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

Let's go ahead and analyze a basket of stocks from the S&P 500 as an investment portfolio. We will import the necessary packages, connect to the database, query the database for our pricing data bind it to the         df_pricing dataframe. Before we procedd any futher, we want to focus on stocks that existed from the start of the 4 year data we stored so that any aggregated return comparison is not skewed by newer stocks that         were traded later on. We will filter the stocks


        # Determine the first date for each ticker
        first_dates = df_pricing.groupby('Ticker')['Date'].min().reset_index()
        first_dates.rename(columns={'Date': 'First Date'}, inplace=True)

        # Count how many tickers share the same first date
        count_first_dates = first_dates['First Date'].value_counts().reset_index()
        count_first_dates.columns = ['First Date', 'Count']

        # Filter for first dates that have more than one ticker
        valid_first_dates = count_first_dates[count_first_dates['Count'] > 1]['First Date']

       # Merge back to keep only those tickers with the same first date
        df_pricing_filtered = df_pricing.merge(first_dates, on='Ticker', suffixes=('', '_y'))  # Specify suffixes here
        df_pricing_filtered = df_pricing_filtered[df_pricing_filtered['First Date'].isin(min_valid_first_date)].copy()

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

Next we extract the daily return dataframe as df_portfolio_pricing for the 10 Tickers that had the highest Annualized Calmar Ratio from our prior Equity perfromance analysis.

        portfolio_tickers= ['LLY','SMCI','TRGP','MCK','MRO','PWR','MPC','XOM','FANG','IRM']
        df_portfolio_pricing = df_pricing_filtered[df_pricing_filtered['Ticker'].isin(portfolio_tickers)].copy()
        ticker_cnt3 = len(df_portfolio_pricing['Ticker'].unique())
        print(f'Portfolio list count: {ticker_cnt3}')

If we want to compare the returns of the S&P 500 Tickers to our portfolio, one way to do this is to use an average return for our portfolio. We will calculate our daily returns as df_ret and calculate the average returns for our portfolio as df_portfolio_ret. We'll assign the Ticker label for our portfolio as 'PFL'.

        df_ret = calculate_return(df_pricing_filtered.copy(), 'Daily')
        df_ret.drop(columns=['Open', 'High', 'Low', 'Close', 'Volume'], inplace=True)
        df_ret.sort_values(by=['Ticker', 'Date'], inplace=True)
        

        
