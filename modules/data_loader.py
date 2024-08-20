import streamlit as st
import pandas as pd
import os

def save_uploaded_file(uploaded_file, output_folder="data"):
    """
    Save the uploaded file to the specified output folder called data and handle file replacement.
    """
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Define the path where the file will be saved
    file_path = os.path.join(output_folder, uploaded_file.name)

    # Save the new file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path

def load_and_convert_to_csv(file_path, sheet_name=None):
    """
    Load an Excel file, convert it to CSV, delete the existing CSV file (if any),
    and save the new one in the specified output folder. Delete the original XLSX file after conversion.
    """
    if file_path.endswith('.xlsx'):
        # Load Excel file with the given sheet name
        data = pd.read_excel(file_path, sheet_name=sheet_name)
        # Prepare CSV file path
        csv_file_path = file_path.replace('.xlsx', '.csv')

        # Delete the existing CSV file if it exists
        if os.path.exists(csv_file_path):
            os.remove(csv_file_path)

        # Convert to CSV and save
        data.to_csv(csv_file_path, index=False)

        # Delete the original XLSX file
        os.remove(file_path)

        return data, csv_file_path

    elif file_path.endswith('.csv'):
        # Load CSV file
        data = pd.read_csv(file_path)
        return data, file_path

    else:
        raise ValueError("Unsupported file format. Please use .xlsx or .csv files.")

def validate_data(data, required_columns, unique_column_name):
    """
    Validate the loaded data by checking for missing columns, duplicate entries, and missing values.
    """
    # Validate required columns
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        st.error(f"Missing columns: {', '.join(missing_columns)}")
        return None

    # Check for duplicate entries in the unique column
    if data[unique_column_name].duplicated().any():
        st.error(f"Duplicate {unique_column_name}s found.")
        return None

    # Check for missing values in required columns
    if data[required_columns].isnull().any().any():
        st.error("Missing values found in required columns.")
        return None

    return data
def handle_invalid_quantities(df, quantity_column, identifier_column):
    """
    Handle invalid quantities: replace blanks with zero, coerce non-numeric values,
    and issue warnings.
    """
    # Replace blanks with zero
    df[quantity_column] = df[quantity_column].fillna(0)

    # Coerce non-numeric quantities to NaN and issue a warning
    invalid_entries = pd.to_numeric(df[quantity_column], errors='coerce').isna()
    if invalid_entries.any():
        invalid_items = df[identifier_column][invalid_entries].tolist()
        st.warning(f"Warning: The following items have non-numeric quantities: {invalid_items}")
        df.loc[invalid_entries, quantity_column] = 0  # Replace with zero after warning

    return df

def handle_invalid_dates(df, date_column, identifier_column):
    """
    Handle invalid dates: coerce to datetime, issue warnings for failed conversions.
    """
    df[date_column] = pd.to_datetime(df[date_column], errors='coerce')

    # Identify and warn about invalid dates
    invalid_dates = df[date_column].isna()
    if invalid_dates.any():
        invalid_items = df[identifier_column][invalid_dates].tolist()
        st.warning(f"Warning: The following items have invalid dates: {invalid_items}")
        df.loc[invalid_dates, date_column] = pd.Timestamp.now()  # Replace with the current date after warning

    return df

def load_raw_materials_master(uploaded_file):
    """
    Load, convert, and validate the Raw Materials Master List.
    """
    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file, output_folder="data")
        raw_materials_data, csv_path = load_and_convert_to_csv(file_path, sheet_name='raw_materials')

        if raw_materials_data is not None:
            required_columns = ['Material Code', 'Material Name', 'Unit of Measure']
            validated_data = validate_data(raw_materials_data, required_columns, 'Material Code')
            return validated_data
    return None

def load_finished_goods_master(uploaded_file):
    """
    Load, convert, and validate the Finished Goods Master List.
    """
    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file, output_folder="data")
        finished_goods_data, csv_path = load_and_convert_to_csv(file_path, sheet_name='finished_goods')

        if finished_goods_data is not None:
            required_columns = ['Product Code', 'Product Name', 'Category', 'Unit of Measure', 'Description']
            validated_data = validate_data(finished_goods_data, required_columns, 'Product Code')
            return validated_data
    return None

def load_bom(uploaded_file, raw_materials_data, finished_goods_data):
    """
    Load, convert, and validate the Bill of Materials (BOM) data. Validate if columns are consistent
    and in agreement with the master list and are mot duplicated. Each Finished goods should use a specific raw material only once.
    We use the unique recipe column to check this.
    """
    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file, output_folder="data")
        bom_data, csv_path = load_and_convert_to_csv(file_path, sheet_name='bill_of_materials')

        if bom_data is not None:
            # Validate that the necessary columns are present
            required_columns = ['Product Code', 'Product Name', 'Material Code', 'Material Name', 'Quantity Required',
                                'Unit of Measure','Unique_Recipe']
            validated_data = validate_data(bom_data, required_columns, 'Unique_Recipe')

            if validated_data is None:
                return None
            # Validate Product Codes against Finished Goods Master List
            invalid_products = bom_data[~bom_data['Product Code'].isin(finished_goods_data['Product Code'])]
            if not invalid_products.empty:
                st.error("Invalid Product Codes found in BOM that are not in Finished Goods Master List.")
                st.dataframe(invalid_products)
                return None

            # Validate Component Codes against Raw Materials Master List
            invalid_components = bom_data[~bom_data['Material Code'].isin(raw_materials_data['Material Code'])]
            if not invalid_components.empty:
                st.error("Invalid Raw Material Codes found in BOM that are not in Raw Materials Master List.")
                st.dataframe(invalid_components)
                return None
            return bom_data
    return None

def load_sales_data(uploaded_file,finished_goods_data):
    """
    Function to load, convert to CSV, and validate the sales data.
    It checks for consistency with the Finished Goods Master List

    """
    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file, output_folder="data")
        sales_data, csv_path = load_and_convert_to_csv(file_path, sheet_name='sales_data')

        if sales_data is not None:
            required_columns = ['Product Code', 'Product Name']
            validated_data = validate_data(sales_data, required_columns, 'Product Code')
            if validated_data is None:
                return None
            # Validate consistency with Finished Goods Master List
            missing_products = set(sales_data['Product Code']) - set(finished_goods_data['Product Code'])
            if missing_products:
                st.error(
                    f"Sales data contains products not listed in the Finished Goods Master List: {missing_products}")
                return None
            return sales_data
        return None, None


def load_raw_materials_inventory(uploaded_file, raw_materials_data):
    """
    Function to load, convert to CSV, and validate the Raw Materials Data.
    It checks for consistency with the Raw Materials Master List, checks the date, and fills blanks with zero.
    """
    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file, output_folder="data")
        raw_materials_inventory, csv_path = load_and_convert_to_csv(file_path, sheet_name='raw_materials_inventory')

        if raw_materials_inventory is not None:
            required_columns = ['Material Code', 'Material Name', 'Unit of Measure', 'Quantity', 'Date']
            validated_data = validate_data(raw_materials_inventory, required_columns, 'Material Code')

            if validated_data is None:
                return None

            # Handle invalid quantities and dates
            validated_data = handle_invalid_quantities(validated_data, 'Quantity', 'Material Name')
            validated_data = handle_invalid_dates(validated_data, 'Date', 'Material Name')

            # Validate consistency with the Raw Materials Master List
            missing_products = set(validated_data['Material Code']) - set(raw_materials_data['Material Code'])
            if missing_products:
                st.error(
                    f"Raw Materials Inventory contains items not listed in the Raw Materials Master List: {missing_products}")
                return None

            return validated_data
        return None


def load_finished_goods_inventory(uploaded_file, finished_goods_data):
    """
    Function to load, convert to CSV, and validate the Finished Goods Data.
    It checks for consistency with the Finished Goods Master List, checks the date, and fills blanks with zero.
    """
    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file, output_folder="data")
        finished_goods_inventory, csv_path = load_and_convert_to_csv(file_path, sheet_name='finished_goods_inventory')

        if finished_goods_inventory is not None:
            required_columns = ['Product Code', 'Product Name', 'Category', 'Unit of Measure', 'Description',
                                'Quantity', 'Date']
            validated_data = validate_data(finished_goods_inventory, required_columns, 'Product Code')

            if validated_data is None:
                return None

            # Handle invalid quantities and dates
            validated_data = handle_invalid_quantities(validated_data, 'Quantity', 'Product Name')
            validated_data = handle_invalid_dates(validated_data, 'Date', 'Product Name')

            # Validate consistency with the Finished Goods Master List
            missing_products = set(validated_data['Product Code']) - set(finished_goods_data['Product Code'])
            if missing_products:
                st.error(
                    f"Finished Goods Inventory contains items not listed in the Finished Goods Master List: {missing_products}")
                return None

            return validated_data
        return None