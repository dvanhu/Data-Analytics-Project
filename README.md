# Retail Orders Data Analysis

This project demonstrates a complete workflow to download, process, and analyze retail orders data using the Kaggle API, Python, and SQL. It covers:

- Setting up Kaggle API credentials  
- Downloading and extracting dataset  
- Data cleaning and feature engineering with Python (pandas)  
- Storing data in SQLite database  
- Running analytical SQL queries for business insights  

---

## Table of Contents

- [Prerequisites](#prerequisites)  
- [Setup Kaggle API](#setup-kaggle-api)  
- [Download and Extract Dataset](#download-and-extract-dataset)  
- [Data Processing with Python](#data-processing-with-python)  
- [Load Data into SQLite](#load-data-into-sqlite)  
- [SQL Queries for Analysis](#sql-queries-for-analysis)  
- [Project Structure](#project-structure)  
- [License](#license)  

---

## Prerequisites

Make sure you have the following installed:

- Python 3.7+  
- pip (Python package manager)  
- SQLite3  

Install required Python packages:

```bash
pip install kaggle pandas sqlalchemy pyodbc

Setup Kaggle API
1.Create a Kaggle account and generate your API token:

- Go to your Kaggle account > Account > API section

- Click Create New API Token, which downloads kaggle.json

2.Place your credentials securely using the Python script below or manually:

import os
import json

kaggle_api = {
    "username": "YOUR_KAGGLE_USERNAME",
    "key": "YOUR_KAGGLE_API_KEY"
}

kaggle_dir = os.path.join(os.path.expanduser('~'), '.kaggle')
os.makedirs(kaggle_dir, exist_ok=True)

with open(os.path.join(kaggle_dir, 'kaggle.json'), 'w') as f:
    json.dump(kaggle_api, f)

os.chmod(os.path.join(kaggle_dir, 'kaggle.json'), 0o600)
print("Kaggle API credentials saved.")

3. You can now download datasets from Kaggle using the kaggle CLI.

Download and Extract Dataset
The dataset orders.csv.zip should be downloaded to ~/.kaggle/.

Extract it programmatically:

import zipfile
import os

zip_path = os.path.join(os.path.expanduser('~'), '.kaggle', 'orders.csv.zip')
extract_to = os.path.join(os.getcwd(), 'retail_orders_data')

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to)

print(f"Dataset extracted to: {extract_to}")


Data Processing with Python
Load CSV into pandas DataFrame

Clean column names (lowercase, replace spaces with underscores)

Create derived columns: discount, sale price, profit

Convert dates to datetime objects

Drop unnecessary columns

Example snippet:

import pandas as pd

csv_path = 'retail_orders_data/orders.csv'
df = pd.read_csv(csv_path, na_values=['Not Available', 'unknown'])

df.columns = df.columns.str.lower().str.replace(' ', '_')
df['discount'] = df['list_price'] * df['discount_percent'] * 0.01
df['sale_price'] = df['list_price'] - df['discount']
df['profit'] = df['sale_price'] - df['cost_price']
df['order_date'] = pd.to_datetime(df['order_date'], format='%Y-%m-%d')

df.drop(columns=['list_price', 'cost_price', 'discount_percent'], inplace=True)


Load Data into SQLite
Store the cleaned DataFrame into a SQLite database for SQL querying:

import sqlite3

conn = sqlite3.connect('mydatabase.db')
df.to_sql('orders', conn, if_exists='replace', index=False)
conn.close()
SQL Queries for Analysis
This project includes several useful SQL queries to analyze the data:

Top 10 highest revenue-generating products

Top 5 best-selling products by region

Month-over-month sales growth comparison between 2022 and 2023

Highest sales month per product category

Sub-category with highest sales growth from 2022 to 2023

Example query:
SELECT TOP 10 
    product_id,
    SUM(sale_price) AS total_sales
FROM orders
GROUP BY product_id
ORDER BY total_sales DESC;
Full SQL queries are available in the queries.sql file for easy reference.

Project Structure
retail-orders-analysis/
│
├── setup_kaggle.py            # Script to set up Kaggle API credentials
├── extract_dataset.py         # Script to extract downloaded dataset
├── data_processing.py         # Python script for cleaning and feature engineering
├── load_to_db.py              # Script to load processed data into SQLite DB
├── queries.sql                # SQL queries for data analysis
├── retail_orders_data/        # Extracted dataset folder (orders.csv)
├── README.md                  # Project overview and instructions (this file)

License
This project is open source and available under the MIT License.


---

You can just copy-paste this in your `README.md` file for a clean, professional GitHub presentation! Want me to help with any script files next?


