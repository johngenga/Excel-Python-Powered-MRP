import streamlit as st
import pandas as pd
import os
from modules import load_raw_materials_master, load_finished_goods_master, load_bom, load_sales_data, load_raw_materials_inventory, load_finished_goods_inventory
from modules.forecasting import holt_winters_cross_validation, holt_winters_forecast_for_products

#Streamlit App

st.title("Materials Requirement Planning Tool")

# Step 1: Upload and Load Raw Materials Master List
st.subheader("Update Raw Materials Master List")
uploaded_raw_materials_file = st.file_uploader("Raw Materials Master List", type=["xlsx", "csv"])
raw_materials_data = pd.read_csv(os.path.join("data","raw_materials_master.csv")).head()

if uploaded_raw_materials_file is not None:
    try:
        raw_materials_data = load_raw_materials_master(uploaded_raw_materials_file)
        st.success("Raw Materials Master List Loaded Successfully")
    except Exception as e:
        st.error(f"Error loading raw materials: {e}")
if raw_materials_data is not None:
    st.write("Preview of Raw Materials Master List:")
    st.dataframe(raw_materials_data.head(3))



# Step 2: Upload and Load Finished Goods Master List
st.subheader("Update Finished Goods Master List")
uploaded_finished_goods_file = st.file_uploader("Upload Finished Goods Master List", type=["xlsx", "csv"])
finished_goods_data = pd.read_csv(os.path.join("data","finished_goods_master.csv")).head()

if uploaded_finished_goods_file is not None:
    try:
        finished_goods_data = load_finished_goods_master(uploaded_finished_goods_file)
        st.success("Finished Goods Data Loaded Successfully")
    except Exception as e:
        st.error(f"Error loading finished goods: {e}")
if finished_goods_data is not None:
    st.write("Preview of Finished Goods Master List:")
    st.dataframe(finished_goods_data.head(3))


# Step 3: Load BOM only if the master lists are valid and successfully loaded
st.subheader("Update Bill of Materials")
raw_materials_data = pd.read_csv(os.path.join("data","raw_materials_master.csv"))
finished_goods_data = pd.read_csv(os.path.join("data","finished_goods_master.csv"))
bom_data = pd.read_csv(os.path.join("data","bill_of_materials.csv"))

uploaded_bom_file = st.file_uploader("Upload Bill of Materials (BOM)", type=["xlsx", "csv"])
if uploaded_bom_file is not None:
    try:
        bom_data = load_bom(uploaded_bom_file, raw_materials_data, finished_goods_data)
        if bom_data is not None:
            st.success("BOM Data Loaded Successfully")

        else:
            st.error("Failed to load BOM data.")
    except Exception as e:
        st.error(f"Error loading BOM: {e}")
if finished_goods_data is not None:
    st.write("Preview of Bill of Materials Master List:")
    st.dataframe(bom_data.head(3))

# Step 4: Load Sales Data and validate it
st.subheader("Update Sales Data")
uploaded_sales_data = st.file_uploader("Upload Sales Data", type=["xlsx", "csv"])
sales_data = pd.read_csv(os.path.join("data","sales_data.csv"))
if uploaded_sales_data is not None and finished_goods_data is not None:
    try:
        sales_data = load_sales_data(uploaded_sales_data, finished_goods_data)
        if sales_data is not None:
            st.success("Sales Data Loaded Successfully")
            st.write(sales_data.head(3))
        else:
            st.error("Failed to load Sales data.")
    except Exception as e:
        st.error(f"Error loading Sales Data: {e}")
if sales_data is not None:
    st.write("Preview of Sales Data:")
    st.dataframe(sales_data.head(3))


# Step 5: Load Raw Materials Inventory and validate it
st.subheader("Update Raw Materials Inventory")
uploaded_raw_materials_inventory = st.file_uploader("Upload Raw Materials Inventory", type=["xlsx", "csv"])
raw_materials_inventory = pd.read_csv(os.path.join("data","raw_materials_inventory.csv"))

if uploaded_raw_materials_inventory is not None and raw_materials_data is not None:
    try:
        raw_materials_inventory = load_raw_materials_inventory(uploaded_raw_materials_inventory, raw_materials_data)
        if raw_materials_inventory is not None:
            st.success("Raw Materials Inventory Loaded Successfully")
            st.write(raw_materials_inventory.head(3))
        else:
            st.error("Failed to load Raw Materials Inventory.")
    except Exception as e:
        st.error(f"Error loading Raw Materials Inventory: {e}")
if raw_materials_inventory is not None:
    st.write("Preview of Raw Materials Inventory:")
    st.dataframe(raw_materials_inventory.head(3))

# Step 6: Load Finished Goods Inventory and validate it
st.subheader("Upload Finished Goods Inventory")
uploaded_finished_goods_inventory = st.file_uploader("Upload Finished Goods Inventory", type=["xlsx", "csv"])
finished_goods_inventory = pd.read_csv(os.path.join("data","finished_goods_inventory.csv"))

if uploaded_finished_goods_inventory is not None and finished_goods_data is not None:
    try:
        finished_goods_inventory = load_finished_goods_inventory(uploaded_finished_goods_inventory, finished_goods_data)
        if finished_goods_inventory is not None:
            st.success("Finished Goods Inventory Loaded Successfully")
            st.write(finished_goods_inventory.head(3))
        else:
            st.error("Failed to load Finished Goods Inventory.")
    except Exception as e:
        st.error(f"Error loading Finished Goods Inventory: {e}")

if finished_goods_inventory is not None:
    st.write("Preview of Finished Goods Inventory:")
    st.dataframe(finished_goods_inventory.head(3))

## FORECASTING ANALYSIS

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




















