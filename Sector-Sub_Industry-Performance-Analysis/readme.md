Let's do some analysis on a Sectors and Sub-Industries. We will also be adding a new function to our *custom_python_functions.py* file which can be re-used in this project. 

## Modify custom re-usable functions: *[custom_python_functions.py](https://github.com/danvuk567/SP500-Stock-Analysis/blob/main/Custom-Python-Functions/custom_python_functions.py)*

Let's define a function called *calculate_portfolio_return* which will plot a **Scatter Plot** using matplotlib and sklearn packages of the our returns and draw a regression line. We will need to install the sklearn package if it has not been installed and import the LinearRegression module from sklearn. This will draw a regression line of our data to predict future outcomes. The function requires a returns dataframe and return type as input parameters.

        from sklearn.linear_model import LinearRegression

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

Let's go ahead and analyze a basket of stocks from the S&P 500 as an investment portfolio. We will import the necessary packages, connect to the database, query the database for our pricing data bind it to the         df_pricing dataframe. Before we proceed any futher, we want to focus on stocks that existed from the start of the 4 year data we stored so that any aggregated return comparison is not skewed by newer stocks that         were traded later on.

