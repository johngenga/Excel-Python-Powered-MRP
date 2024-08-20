import streamlit as st
import pandas as pd
import os
from modules import load_raw_materials_master, load_finished_goods_master, load_bom, load_sales_data, load_raw_materials_inventory, load_finished_goods_inventory
from modules.forecasting import holt_winters_cross_validation, holt_winters_forecast_for_products

# Streamlit App
# Here is where we use the App to run the project

header = st.container()
dataset = st.container()
forecast = st.container()
with header:
    st.title("Materials Requirement Planning")
    st.write("This is a simple and user-friendly App for forecasting raw materials requirement by simply uploading afew snapshots of the current inventory status and settings in excel format. ")

with dataset:
    # DATASETS: In this section we are uploading the excel files that will be used,
    # converting them to csv and doing clean-up where necessary.


    # Step 1: Upload and Update Raw Materials Master List
    st.subheader("Upload and Update the Data Sets")
    st.write("In this section we upload the datasets. All the datasets can be uploaded as excel or csv files")

    st.markdown(
        "**Update the Raw Materials Master File** - "
        "This file creates a standardized list of raw materials. The columns depicted are mandatory"
    )
    # Set Col structure
    sel_col, disp_col = st.columns(2)
    uploaded_raw_materials_file = sel_col.file_uploader("Raw Materials Master", type=["xlsx", "csv"])
    raw_materials_data = pd.read_csv(os.path.join("data","raw_materials_master.csv")).head()

    if uploaded_raw_materials_file is not None:
        try:
            raw_materials_data = load_raw_materials_master(uploaded_raw_materials_file)
            sel_col.success("Raw Materials Master List Loaded Successfully")
        except Exception as e:
            sel_col.error(f"Error loading raw materials: {e}")
    if raw_materials_data is not None:
        disp_col.markdown("Preview of Raw Materials Master List:")
        disp_col.dataframe(raw_materials_data.head())

    # Step 2: Upload and Update Finished Goods Master List
    st.markdown(
        "**Update the Finished Goods Master File** - "
        "This file creates a standardized list of Finished Goods. The columns depicted are mandatory"
    )
    # Set Col structure
    sel_col, disp_col = st.columns(2)
    uploaded_finished_goods_file = sel_col.file_uploader("Upload Finished Goods Master List", type=["xlsx", "csv"])
    finished_goods_data = pd.read_csv(os.path.join("data","finished_goods_master.csv")).head()

    if uploaded_finished_goods_file is not None:
        try:
            finished_goods_data = load_finished_goods_master(uploaded_finished_goods_file)
            sel_col.success("Finished Goods Data Loaded Successfully")
        except Exception as e:
            sel_col.error(f"Error loading finished goods: {e}")
    if finished_goods_data is not None:
        disp_col.write("Preview of Finished Goods Master List:")
        disp_col.dataframe(finished_goods_data.head())


    # Step 3: Load BOM only if the master lists are valid and successfully loaded
    st.markdown(
        "**Update the Bill of Materials** - "
        "This file creates a standardized list that assigns"
        "raw materials to finished goods. The raw materials and the "
        "finished goods need to be mapped to the master files"
    )
    # Set Col structure
    sel_col, disp_col = st.columns(2)
    raw_materials_data = pd.read_csv(os.path.join("data","raw_materials_master.csv"))
    finished_goods_data = pd.read_csv(os.path.join("data","finished_goods_master.csv"))
    bom_data = pd.read_csv(os.path.join("data","bill_of_materials.csv"))

    uploaded_bom_file = sel_col.file_uploader("Upload Bill of Materials (BOM)", type=["xlsx", "csv"])
    if uploaded_bom_file is not None:
        try:
            bom_data = load_bom(uploaded_bom_file, raw_materials_data, finished_goods_data)
            if bom_data is not None:
                sel_col.success("BOM Data Loaded Successfully")
            else:
                sel_col.error("Failed to load BOM data.")
        except Exception as e:
            sel_col.error(f"Error loading BOM: {e}")
    if finished_goods_data is not None:
        disp_col.write("Preview of Bill of Materials Master List:")
        disp_col.dataframe(bom_data.head())

    # Step 4: Load Sales Data and validate it
    st.markdown(
        "**Update the Sales Data** - "
        "This is a record from historical sales from periods prior to the forecast date. "
        "Using python machine learning libraries, this data will be used to "
        "create the sales forecast of finished goods"
    )
    # Set Col structure
    sel_col, disp_col = st.columns(2)
    uploaded_sales_data = sel_col.file_uploader("Upload Sales Data", type=["xlsx", "csv"])
    sales_data = pd.read_csv(os.path.join("data","sales_data.csv"))
    if uploaded_sales_data is not None and finished_goods_data is not None:
        try:
            sales_data = load_sales_data(uploaded_sales_data, finished_goods_data)
            if sales_data is not None:
                sel_col.success("Sales Data Loaded Successfully")
            else:
                sel_col.error("Failed to load Sales data.")
        except Exception as e:
            sel_col.error(f"Error loading Sales Data: {e}")
    if sales_data is not None:
        disp_col.write("Preview of Sales Data:")
        disp_col.dataframe(sales_data.head())

    # Step 5: Load Raw Materials Inventory and validate it
    st.markdown(
        "**Update Raw Materials Inventory** - "
        "This is a record Raw Materials stock in hand as at a specific date. "
        "The date is a snapshot as close as possible to the date when the sales"
        "records are uploaded."
    )
    # Set Col structure
    sel_col, disp_col = st.columns(2)
    uploaded_raw_materials_inventory = sel_col.file_uploader("Uploaded Raw Materials Inventory", type=["xlsx", "csv"])
    raw_materials_inventory = pd.read_csv(os.path.join("data","raw_materials_inventory.csv"))

    if uploaded_raw_materials_inventory is not None and raw_materials_data is not None:
        try:
            raw_materials_inventory = load_raw_materials_inventory(uploaded_raw_materials_inventory, raw_materials_data)
            if raw_materials_inventory is not None:
                sel_col.success("Raw Materials Inventory Loaded Successfully")
            else:
                sel_col.error("Failed to load Raw Materials Inventory.")
        except Exception as e:
            sel_col.error(f"Error loading Raw Materials Inventory: {e}")
    if raw_materials_inventory is not None:
        disp_col.write("Preview of Raw Materials Inventory:")
        disp_col.dataframe(raw_materials_inventory.head())

with dataset:
    # Step 6: Load Finished Goods Inventory and validate it
    st.markdown(
        "**Update Finished Goods Inventory** - "
        "This is a record stock Finished Goods in hand as at a specific date. "
        "The date is a snapshot as close as possible to the date when the sales"
        "records are uploaded."
    )
    # Set Col structure
    sel_col, disp_col = st.columns(2)
    uploaded_finished_goods_inventory = sel_col.file_uploader("Uploaded Finished Goods Inventory", type=["xlsx", "csv"])
    finished_goods_inventory = pd.read_csv(os.path.join("data","finished_goods_inventory.csv"))

    if uploaded_finished_goods_inventory is not None and finished_goods_data is not None:
        try:
            finished_goods_inventory = load_finished_goods_inventory(uploaded_finished_goods_inventory, finished_goods_data)
            if finished_goods_inventory is not None:
                sel_col.success("Finished Goods Inventory Loaded Successfully")
            else:
                sel_col.error("Failed to load Finished Goods Inventory.")
        except Exception as e:
            sel_col.error(f"Error loading Finished Goods Inventory: {e}")
    if finished_goods_inventory is not None:
        disp_col.write("Preview of Finished Goods Inventory:")
        disp_col.dataframe(finished_goods_inventory.head())

with forecast:
    ###  FORECASTING
    # Step 7: Holt Winters Average RMSE.
    st.subheader("Forecasting Calculations")
    st.write("Holt-Winters Forecasting Average RMSE Cross Validation Calculator")
    df = os.path.join("data", "sales_data.csv")

    if sales_data is not None:
        try:
            holt_winters_average_rmse = holt_winters_cross_validation(df)
            st.success(f"Average RMSE across all products: {holt_winters_average_rmse:.3f}")
            holt_winters_365 = holt_winters_forecast_for_products(df)
            st.write("Holt-Winters Sales forecast for the next 365 days")
            st.dataframe(holt_winters_365)
        except Exception as e:
            st.error(f"Error calculating RMSE: {e}")