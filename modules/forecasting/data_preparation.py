# Centralizing data processing.
import pandas as pd


def prepare_sales_data(file_path):
    """

    :param file_path: Path to the uploaded sales file in the data folder.
    :return: Root Mean Squared Error for all unique products presented as an average to evaluate the model
    """
    # Load the sales data
    df = pd.read_csv(file_path)
    df = pd.melt(
        df,
        id_vars=['Product Code', 'Product Name'],
        var_name='Date',
        value_name='Sales'
    )
    # Convert date columns to periods
    df['Date'] = pd.to_datetime(df['Date'])
    return df


def prepare_features(file_path):
    df = prepare_sales_data(file_path)
    # Date features
    df['weekday'] = pd.to_datetime(df['Date']).dt.weekday
    df['month'] = pd.to_datetime(df['Date']).dt.month
    df['year'] = pd.to_datetime(df['Date']).dt.year
    df['dayofyear'] = pd.to_datetime(df['Date']).dt.dayofyear
    df['weekofyear'] = pd.to_datetime(df['Date']).dt.isocalendar().week

    # Rolling window features Fill NaNs in rolling features with the overall mean and std
    # (assuming that initial periods can use overall stats)
    df['rolling_mean_7'] = df.groupby(['Product Code', 'Product Name'])['Sales'].shift(1).rolling(
        window=7).mean().fillna(df['Sales'].mean())
    df['rolling_mean_30'] = df.groupby(['Product Code', 'Product Name'])['Sales'].shift(1).rolling(
        window=30).mean().fillna(df['Sales'].mean())
    df['rolling_std_7'] = df.groupby(['Product Code', 'Product Name'])['Sales'].shift(1).rolling(window=7).std().fillna(
        df['Sales'].mean())
    df['rolling_std_30'] = df.groupby(['Product Code', 'Product Name'])['Sales'].shift(1).rolling(
        window=30).std().fillna(df['Sales'].mean())
    return df

