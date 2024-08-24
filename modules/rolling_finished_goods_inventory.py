
import pandas as pd
import os
from modules.forecasting.data_preparation import prepare_sales_data

""" 
Here take the sales data and merge it with the stock data so that the 'Product Code', 'Product name' and 'Date' merge
can form a point for determining finished goods variances.
Step 1: Understand the Data

    finished_goods_inventory DataFrame: Contains the initial stock (Quantity) and the date (Date) of stock take.
    sales_data_merged DataFrame: Contains sales forecasts, quantities, and stock deltas (which indicate changes in 
    inventory).

Step 2: Identify the Relevant Date Range

We need to identify the first date of stock take (from finished_goods_inventory) and the last date from the 
sales_data_merged DataFrame.
Step 3: Initialize the Inventory DataFrame

We’ll create a new DataFrame to hold the cumulative inventory over the date range.
Step 4: Iterate Over the Dates and Update the Inventory

We will update the inventory based on the Stock_delta for each day.
Step 5: Create the Final Inventory DataFrame

"""


def rolling_finished_goods():
    # Process the sales data for the calculation.
    sales_data = prepare_sales_data(os.path.join("data", "forecast.csv"))

    # Read the finished goods inventory and parse the dates into DateTime format.
    finished_goods_inventory = pd.read_csv(os.path.join("data", "finished_goods_inventory.csv"))
    finished_goods_inventory['Date'] = pd.to_datetime(finished_goods_inventory['Date'])

    # Merge inventory data with sales data forecast on the date of inventory counts.
    # The start of the forecast should not be later than the inventory counts date.
    sales_data_merged = sales_data.merge(finished_goods_inventory, on=['Product Code', 'Product Name', 'Date'],
                                         how='left')

    # Retain relevant columns and remove irrelevant columns for the MRP calculation.
    # Create column showing difference between forecast and inventory.
    sales_data_merged = sales_data_merged.drop(columns=['Category', 'Unit of Measure', 'Description'])
    sales_data_merged['Quantity'] = sales_data_merged['Quantity'].fillna(0)
    sales_data_merged['Stock_delta'] = sales_data_merged['Quantity'] - sales_data_merged['Sales']

    # Assuming `sales_data_merged` and `finished_goods_inventory` are already loaded

    # start_date should be the date of stock take (the first date in finished_goods_inventory['Date'])
    start_date = finished_goods_inventory['Date'].min()

    # Get the last date in the sales_data_merged DataFrame
    end_date = sales_data_merged['Date'].max()

    # Create a date range from start_date to end_date
    date_range = pd.date_range(start=start_date, end=end_date)

    # Initialize the inventory DataFrame with Product Code and Product Name as a MultiIndex
    inventory_df = pd.DataFrame(
        index=pd.MultiIndex.from_frame(finished_goods_inventory[['Product Code', 'Product Name']].drop_duplicates()),
        columns=date_range)

    # Set the initial stock for the start_date
    for index, row in finished_goods_inventory.iterrows():
        product_code = row['Product Code']
        product_name = row['Product Name']
        inventory_df.loc[(product_code, product_name), start_date] = row['Quantity']

    # Fill the rest of the dates with cumulative inventory
    for i in range(1, len(date_range)):
        current_date = date_range[i]
        previous_date = date_range[i - 1]

        # First, copy the previous day's inventory to the current day
        inventory_df[current_date] = inventory_df[previous_date]

        # Apply stock delta changes from sales_data_merged for the current date
        daily_sales_data = sales_data_merged[sales_data_merged['Date'] == current_date]

        for index, row in daily_sales_data.iterrows():
            product_code = row['Product Code']
            product_name = row['Product Name']
            inventory_df.loc[(product_code, product_name), current_date] += row['Stock_delta']

    # Fill NaN values in inventory_df with the last valid inventory value (carry forward stock levels)
    inventory_df = inventory_df.ffill(axis=1)

    # Ensure the correct dtype inference after forward fill
    inventory_df = inventory_df.infer_objects(copy=False)

    # Save the forecast DataFrame to a CSV file in the 'data' folder
    save_inventory_df_to_csv(inventory_df, output_folder="data", filename="rolling_finished_goods.csv")

    return inventory_df


def save_inventory_df_to_csv(inventory_df, output_folder="data", filename="rolling_finished_goods.csv"):
    # Check if the output folder exists; if not, create it
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define the full path for the CSV file
    file_path = os.path.join(output_folder, filename)

    # Save the DataFrame to a CSV file
    inventory_df.to_csv(file_path, index=True)
