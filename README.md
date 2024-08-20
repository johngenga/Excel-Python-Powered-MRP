# Excel-Python-Powered-MRP
Supply Chain Planning Tool
Overview

The Supply Chain Planning Tool is a Python-based application designed to optimize supply chain processes by integrating key functionalities like forecasting, materials requirement planning (MRP), and inventory management. The tool allows users to upload and analyze data from various Excel files to make informed decisions about production scheduling, material procurement, and inventory management.
Features

    Sales Forecasting: Generate forecasts using various time series models, including Holt-Winters and XGBoost. The tool provides graphical visualization of historical and forecasted sales data, with options to view data daily, weekly, or monthly.
    Materials Requirement Planning (MRP): Convert sales forecasts into raw material requirements using the Bill of Materials (BOM). The tool checks stock levels and suggests procurement actions to ensure smooth production.
    Data Handling: Upload Excel files for BOM, sales data, production plans, and stock levels. The tool converts these files to CSV format for analysis and deletes the original files.
    Modular Design: The tool is designed in a modular format, allowing for easy updates and the addition of new features.
    Streamlit Dashboard: Interactive dashboard built using Streamlit, providing a user-friendly interface for data upload, analysis, and visualization.

Getting Started
Prerequisites

    Python 3.x
    Streamlit
    Pandas
    NumPy
    Scikit-learn
    XGBoost
    Statsmodels

Installation

    Clone the repository:

    bash

git clone https://github.com/johngenga/Excel-Python-Powered-MRP
cd supply-chain-planning-tool

Create a virtual environment and activate it:

bash

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required packages:

bash

    pip install -r requirements.txt

Usage

    Upload Data Files: Use the Streamlit interface to upload the required Excel files for BOM, sales data, production plans, and stock levels.
    Generate Forecasts: Choose a forecasting model and generate sales forecasts based on the uploaded data. Visualize the results using the interactive dashboard.
    Run MRP: Convert the sales forecast into raw material requirements and get suggestions on procurement actions.
    Save Results: Save the forecast and MRP results to CSV for further analysis or reporting.

File Structure

    data/: Contains the uploaded and converted CSV files.
    src/: Source code for the tool, including modules for forecasting, MRP, and data handling.
    dashboard/: Streamlit dashboard files.
    docs/: Documentation for the project.
    README.md: This file.
    .gitignore: Specifies files to be ignored by Git.

Contributing

Contributions are welcome! Please follow these steps:

    Fork the repository.
    Create a new branch (git checkout -b feature-branch).
    Make your changes and commit them (git commit -m 'Add some feature').
    Push to the branch (git push origin feature-branch).
    Open a pull request.

License

This project is licensed under the MIT License - see the LICENSE file for details.
Contact

For any inquiries or support, please contact:

    Name: John Genga
    Email: john.genga@gmail.com
    LinkedIn: John Genga


