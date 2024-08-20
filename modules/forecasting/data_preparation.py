# Centralizing data processing.
import pandas as pd
import os


def prepare_sales_data(file_path):
    # Load the sales data
    df = pd.read_csv(file_path)
    df = pd.melt(df, id_vars=['Product Code', 'Product Name'], var_name='Date', value_name='Sales')
    # Example data preparation steps
    # Convert date columns to periods
    df['Date'] = pd.to_datetime(df['Date'])

    # Potentially other preprocessing like filling missing values, etc.
    # df = ...
    return df