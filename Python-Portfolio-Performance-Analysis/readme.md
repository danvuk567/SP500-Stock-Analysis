Let's do some analysis on a portfolio of stocks. We will adding new functions to our *custom_python_functions.py* file which can be re-used in this project. 

## Modify custom re-usable functions: *[custom_python_functions.py](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Custom-Python-Functions/custom_python_functions.py)*

If we want to see how the returns are distributed for a particular Ticke, we can plot it as a **Histogram** using the matplotlib package. This function called *plot_return_histogram* will plot a histogram and calculate the number of bins based on the Freedman-Diaconis rule that uses quartile range. For more information on this rule. refer to this link: [Freedman–Diaconis rule
(https://en.wikipedia.org/wiki/Freedman%E2%80%93Diaconis_rule). To compare how the returns measure up against all the returns that are normalized and plotted as a line representing a Normal Distribution. The scipy package would need to be installed if it isn’t installed. Another line can be drawn that can smooth the ticker return using the Gaussion KDE (Kernel Density Estimation) function from the scipy package. For more informtion on this, refer to this link: [Kernel density estimation](https://en.wikipedia.org/wiki/Kernel_density_estimation). The function takes the return dataframe, return_type and ticker as input parameters.


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



This function called *plot_period_returns_by_ticker_box_plot* creates box plots using the seaborn package of % Returns by period type for Tickers side by side. It takes the return dataframe and period type as input paramters.

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
