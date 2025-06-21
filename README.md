
# WMS - Warehouse Management System (SKU to MSKU Mapper)

This is a Streamlit-based web application that allows you to map SKU values from sales data to their corresponding MSKUs using a mapping Excel file.

## Features

- Upload multiple sales files (.xlsx)
- Upload a SKU to MSKU mapping file (.xlsx)
- Auto-map SKUs to MSKUs
- Download combined mapped result
- View visual chart of MSKU vs Quantity

## How to Run

1. Upload your mapping file
2. Upload all your sales files
3. View results and download the combined CSV
4. Visualize sales distribution by MSKU

## Deployment

To deploy this on Streamlit Cloud:

- Push this repo to GitHub
- Go to https://streamlit.io/cloud
- Connect GitHub and select `app.py`
