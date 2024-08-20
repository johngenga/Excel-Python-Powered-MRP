from .data_preparation import prepare_sales_data
import os
import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_squared_error
from math import sqrt


def holt_winters_cross_validation(df, n_splits=5):
    df = os.path.join("data", "sales_data.csv")
    df = prepare_sales_data(df)
    product_codes = df['Product Code'].unique()
    product_names = df['Product Name'].unique()

    all_errors = []

    for product_code, product_name in zip(product_codes, product_names):
        # Filter the data for the specific product
        product_data = df.loc[(df['Product Code'] == product_code) &
                              (df['Product Name'] == product_name)].copy()

        # Set 'Date' as the index and convert to PeriodIndex with daily frequency
        product_data['Date'] = pd.to_datetime(product_data['Date'])  # Ensure it's datetime first
        product_data.set_index('Date', inplace=True)
        product_data.index = product_data.index.to_period('D')  # Convert the index to PeriodIndex

        # Split the data into train and test
        total_points = len(product_data)
        split_size = total_points // n_splits

        product_errors = []

        for i in range(n_splits):
            train_end = (i + 1) * split_size
            train_data = product_data.iloc[:train_end]
            test_data = product_data.iloc[train_end:train_end + split_size]

            if len(test_data) == 0:
                continue

            # Fit the Holt-Winters model
            model = ExponentialSmoothing(train_data['Sales'], trend='add', seasonal='add', seasonal_periods=12).fit()

            # Predict the next values
            forecast = model.forecast(len(test_data))

            # Calculate RMSE for this split
            rmse = sqrt(mean_squared_error(test_data['Sales'], forecast))
            product_errors.append(rmse)

        # Calculate the average RMSE for this product and add to the list
        avg_product_rmse = np.mean(product_errors)
        all_errors.append(avg_product_rmse)

    # Calculate the average RMSE across all products
    overall_avg_rmse = np.mean(all_errors)
    return overall_avg_rmse

def holt_winters_forecast_for_products(df, forecast_days=365):
    df = os.path.join("data", "sales_data.csv")
    df = prepare_sales_data(df)
    product_codes = df['Product Code'].unique()
    product_names = df['Product Name'].unique()

    forecasts = []

    for product_code, product_name in zip(product_codes, product_names):
        # Filter the data for the specific product
        product_data = df.loc[(df['Product Code'] == product_code) &
                                             (df['Product Name'] == product_name)].copy()

        # Set 'Date' as the index and convert to PeriodIndex with daily frequency
        product_data['Date'] = pd.to_datetime(product_data['Date'])  # Ensure it's datetime first
        product_data.set_index('Date', inplace=True)
        product_data.index = product_data.index.to_period('D')  # Convert the index to PeriodIndex

        # Fit the Holt-Winters model
        model = ExponentialSmoothing(product_data['Sales'], trend='add', seasonal='add', seasonal_periods=12).fit()

        # Forecast the next `forecast_days` days
        forecast = model.forecast(forecast_days)

        # Round the forecasted values and replace any values less than zero with zero
        forecast = forecast.round().clip(lower=0)

        # Store the forecast in a list of dictionaries
        forecast_dict = {
            'Product Code': product_code,
            'Product Name': product_name,
        }

        # Add the forecasted values to the dictionary with dates as keys
        for i, value in enumerate(forecast):
            forecast_date = (product_data.index[-1] + pd.Timedelta(days=i + 1)).strftime('%Y-%m-%d')
            forecast_dict[forecast_date] = value

        forecasts.append(forecast_dict)

    # Convert the list of dictionaries into a DataFrame
    forecast_df = pd.DataFrame(forecasts)

    return forecast_df
