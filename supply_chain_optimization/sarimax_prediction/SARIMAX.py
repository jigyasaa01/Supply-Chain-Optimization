import matplotlib.pyplot
import matplotlib.pyplot
import matplotlib.pyplot


def sarimax(path):
    import pandas as pd
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    import matplotlib
    matplotlib.use('Agg')
    import os
    from pandas.tseries.offsets import DateOffset


    # Create a folder to save the plots
    folder_path_plots = os.path.join(os.path.dirname(path), 'plots')
    if not os.path.exists(folder_path_plots):
        os.makedirs(folder_path_plots)

    folder_path_csv = os.path.join(os.path.dirname(path), 'csv')
    if not os.path.exists(folder_path_csv):
        os.makedirs(folder_path_csv)   
    
    print(folder_path_csv)
    print(folder_path_plots)

    # Load multivariate sales data from CSV file
    sales_data = pd.read_csv(path, parse_dates=['Dates'], index_col='Dates')

    # List of product names
    products = sales_data.columns

    # Iterate over each product and train SARIMAX model
    for product in products:
        # Train SARIMAX model
        model = SARIMAX(sales_data[product], order=(5,1,0), seasonal_order=(1,1,1,12))  # SARIMAX(p,d,q)(P,D,Q,s)
        model_fit = model.fit()

        # Forecast future sales
        n_forecast_steps = 12  # Forecasting sales for the next 12 months
        forecast = model_fit.forecast(steps=n_forecast_steps)
        

        # Visualize past sales and forecasted sales for each product separately
        matplotlib.pyplot.figure(figsize=(12, 6))
        matplotlib.pyplot.plot(sales_data.index, sales_data[product], label='Past Sales', color='#041723')
        matplotlib.pyplot.plot(pd.date_range(start=sales_data.index[-1], periods=n_forecast_steps , freq='ME')[0:], forecast, label='Forecasted Sales', linestyle='-', color='#e37439')
        matplotlib.pyplot.xlabel('Date')
        matplotlib.pyplot.ylabel('Sales')
        matplotlib.pyplot.title(f'SARIMAX Forecast of Future Sales for Product: {product}')
        matplotlib.pyplot.legend()
        matplotlib.pyplot.grid(True)

        plot_path = os.path.join(folder_path_plots, f'{product}_plot.png')
        matplotlib.pyplot.savefig(plot_path)  # Increase dpi for a larger image

        # Close the plot to release memory
        matplotlib.pyplot.close()


        forecast_dates = pd.date_range(start=sales_data.index[-1] + DateOffset(months=1), periods=n_forecast_steps, freq='ME')
        forecast_dates = forecast_dates.strftime('%d/%m/%Y')
        forecast = pd.DataFrame({'Dates': forecast_dates, f'{product}': forecast})
        print(f'Product: {product}')
        print(f'Forecasted Sales:\n {forecast}\n')

        forecast.to_csv(os.path.join(folder_path_csv, f'{product}_forecast.csv'), index=False)

        


# sarimax('/Users/harshit/Desktop/MinorProject_SupplyChain/SalesData1.csv')