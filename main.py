import streamlit as st
import pandas as pd
import os
from modules import (load_raw_materials_master, load_finished_goods_master, load_bom, load_sales_data,
                     load_raw_materials_inventory, load_finished_goods_inventory)
from modules.forecasting import holt_winters_cross_validation, holt_winters_forecast_for_products

# Streamlit App

header = st.container()
dataset = st.container()
forecast = st.container()

with header:
    st.title("Materials Requirement Planning")
    st.info("This App is used for forecasting demand of finished goods and raw materials requirements"
            " by simply uploading afew snapshots of the current inventory status in excel or csv format. ")

with dataset:
    # DATASETS: In this section we are uploading the Excel files that will be used,
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
    raw_materials_data = pd.read_csv(os.path.join("data", "raw_materials_master.csv")).head()

    if uploaded_raw_materials_file is not None:
        try:
            raw_materials_data = load_raw_materials_master(uploaded_raw_materials_file)
            sel_col.success("Raw Materials Master List Loaded Successfully")
        except Exception as e:
            sel_col.error(f"Error loading raw materials: {e}")
    if raw_materials_data is not None:
        disp_col.write("Preview of Raw Materials Master:")
        disp_col.write(raw_materials_data.head())
        disp_col.download_button(
            label="Download Raw Materials Master csv",
            data=open(os.path.join("data", "raw_materials_master.csv"), "rb"),
            file_name="raw_materials_master.csv",
            mime="text/csv"
        )

    # Step 2: Upload and Update Finished Goods Master List
    st.markdown(
        "**Update the Finished Goods Master File** - "
        "This file creates a standardized list of Finished Goods. The columns depicted are mandatory"
    )
    # Set Col structure
    sel_col, disp_col = st.columns(2)
    uploaded_finished_goods_file = sel_col.file_uploader("Upload Finished Goods Master List", type=["xlsx", "csv"])
    finished_goods_data = pd.read_csv(os.path.join("data", "finished_goods_master.csv")).head()

    if uploaded_finished_goods_file is not None:
        try:
            finished_goods_data = load_finished_goods_master(uploaded_finished_goods_file)
            sel_col.success("Finished Goods Master Loaded Successfully")
        except Exception as e:
            sel_col.error(f"Error loading finished goods: {e}")
    if finished_goods_data is not None:
        disp_col.write("Preview of Finished Goods Master:")
        disp_col.write(finished_goods_data.head())
        disp_col.download_button(
            label="Download Finished Goods Master csv",
            data=open(os.path.join("data", "finished_goods_master.csv"), "rb"),
            file_name="finished_goods_master.csv",
            mime="text/csv"
        )

    # Step 3: Load BOM only if the master lists are valid and successfully loaded
    st.markdown(
        "**Update the Bill of Materials** - "
        "This file creates a standardized list that assigns"
        "raw materials to finished goods. The raw materials and the "
        "finished goods need to be mapped to the master files"
    )
    # Set Col structure
    sel_col, disp_col = st.columns(2)
    raw_materials_data = pd.read_csv(os.path.join("data", "raw_materials_master.csv"))
    finished_goods_data = pd.read_csv(os.path.join("data", "finished_goods_master.csv"))
    bom_data = pd.read_csv(os.path.join("data", "bill_of_materials.csv"))

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
    if bom_data is not None:
        disp_col.write("Preview of Bill of Materials:")
        disp_col.write(bom_data.head())
        disp_col.download_button(
            label="Download Bill of Materials csv",
            data=open(os.path.join("data", "bill_of_materials.csv"), "rb"),
            file_name="bill_of_materials.csv",
            mime="text/csv"
        )

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
    sales_data = pd.read_csv(os.path.join("data", "sales_data.csv"))
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
        disp_col.write(sales_data.head())
        disp_col.download_button(
            label="Download Sales Data csv",
            data=open(os.path.join("data", "sales_data.csv"), "rb"),
            file_name="sales_data.csv",
            mime="text/csv"
        )

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
    raw_materials_inventory = pd.read_csv(os.path.join("data", "raw_materials_inventory.csv"))

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
        # Providing option to download csv file to use as template.
        disp_col.write("Preview of Raw materials Inventory:")
        disp_col.write(raw_materials_inventory.head())
        disp_col.download_button(
            label="Download Raw Materials Inventory csv",
            data=open(os.path.join("data", "raw_materials_inventory.csv"), "rb"),
            file_name="raw_materials_inventory.csv",
            mime="text/csv"
        )

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
    finished_goods_inventory = pd.read_csv(os.path.join("data", "finished_goods_inventory.csv"))

    if uploaded_finished_goods_inventory is not None and finished_goods_data is not None:
        try:
            finished_goods_inventory = load_finished_goods_inventory(uploaded_finished_goods_inventory,
                                                                     finished_goods_data)
            if finished_goods_inventory is not None:
                sel_col.success("Finished Goods Inventory Loaded Successfully")
            else:
                sel_col.error("Failed to load Finished Goods Inventory.")
        except Exception as e:
            sel_col.error(f"Error loading Finished Goods Inventory: {e}")
    if finished_goods_inventory is not None:
        # Providing option to download csv file to use as template.
        disp_col.write("Preview of Finished Goods Inventory:")
        disp_col.write(finished_goods_inventory.head())
        disp_col.download_button(
            label="Download Finished Goods Inventory csv",
            data=open(os.path.join("data", "finished_goods_inventory.csv"), "rb"),
            file_name="finished_goods_inventory.csv",
            mime="text/csv"
        )

with forecast:
    st.subheader("Forecasting Calculations")
    st.write("Holt-Winters Forecasting")
    df = os.path.join("data", "sales_data.csv")

    # Button to calculate Holt-Winters Average RMSE
    if st.button("Calculate Holt-Winters Average RMSE"):
        with st.spinner("Calculating RMSE..."):
            try:
                holt_winters_average_rmse = holt_winters_cross_validation()
                st.success(f"Average RMSE across all products: {holt_winters_average_rmse:.3f}")
            except Exception as e:
                st.error(f"Error calculating RMSE: {e}")

    # Button to generate Holt-Winters forecast for the next 365 days
    if st.button("Generate 365-Day Holt-Winters Forecast"):
        with st.spinner("Generating forecast..."):
            try:
                # Generate and save the forecast
                holt_winters_365 = holt_winters_forecast_for_products()

            except Exception as e:
                st.error(f"Error generating forecast: {e}")
    if os.path.join("data", "forecast.csv") is not None:
        # Display the forecast in Streamlit
        st.write("Holt-Winters Sales forecast for the next 365 days")
        st.write(pd.read_csv(os.path.join("data", "forecast.csv")))
        # Provide a download link for the CSV file
        csv_file_path = os.path.join("data", "forecast.csv")
        st.write(f"Forecast saved to {csv_file_path}")
        st.download_button(
            label="Download Forecast CSV",
            data=open(csv_file_path, "rb"),
            file_name="forecast.csv",
            mime="text/csv"
        )