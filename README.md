# Retail Orders Data Analysis

This project demonstrates a complete workflow to download, process, and analyze retail orders data using the Kaggle API, Python, and SQL. It covers:
![Workflow Diagram](https://github.com/user-attachments/assets/8a52c43f-ba27-4337-b1f9-99a4534ab01d)


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


---

## Prerequisites

Make sure you have Python 3.7+ installed along with pip and SQLite3.

Install required Python packages:

```bash
pip install kaggle pandas sqlalchemy pyodbc
```
### Setup Kaggle API
Create a Kaggle account and generate your API token:

Go to your Kaggle account > Account > API section

Click Create New API Token to download kaggle.json

Save your credentials securely using this script:

```python
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
```
### Download and Extract Dataset
Download the dataset orders.csv.zip to the ~/.kaggle/ directory using Kaggle CLI.

Then extract the dataset programmatically:

```python

import zipfile
import os

zip_path = os.path.join(os.path.expanduser('~'), '.kaggle', 'orders.csv.zip')
extract_to = os.path.join(os.getcwd(), 'retail_orders_data')

with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to)

print(f"Dataset extracted to: {extract_to}")

```
### Data Processing with Python
Now clean and process the data using pandas:

```python

import pandas as pd

csv_path = 'retail_orders_data/orders.csv'
df = pd.read_csv(csv_path, na_values=['Not Available', 'unknown'])

df.columns = df.columns.str.lower().str.replace(' ', '_')
df['discount'] = df['list_price'] * df['discount_percent'] * 0.01
df['sale_price'] = df['list_price'] - df['discount']
df['profit'] = df['sale_price'] - df['cost_price']
df['order_date'] = pd.to_datetime(df['order_date'], format='%Y-%m-%d')

df.drop(columns=['list_price', 'cost_price', 'discount_percent'], inplace=True)
```
### Load Data into SQLite
Push the cleaned data into a local SQLite database:

```python

import sqlite3

conn = sqlite3.connect('mydatabase.db')
df.to_sql('orders', conn, if_exists='replace', index=False)
conn.close()
```
### SQL Queries for Analysis
Run SQL queries to generate insights such as:

Top 10 highest revenue-generating products

Top 5 best-selling products by region

Monthly sales comparison between 2022 and 2023

Highest sales month per product category

Sub-category with highest growth rate

Example query to find top 10 products by sales:

```sql

SELECT 
    product_id,
    SUM(sale_price) AS total_sales
FROM orders
GROUP BY product_id
ORDER BY total_sales DESC
LIMIT 10;
```
### Project Structure
```graphql

retail-orders-analysis/
│
├── setup_kaggle.py            # Script to set up Kaggle API credentials
├── extract_dataset.py         # Script to extract downloaded dataset
├── data_processing.py         # Python script for cleaning and feature engineering
├── load_to_db.py              # Script to load processed data into SQLite DB
├── queries.sql                # SQL queries for data analysis
├── retail_orders_data/        # Extracted dataset folder (orders.csv)
├── README.md                  # Project overview and instructions (this file)
```
✅ Output will be a **clean, structured README** in **one cell**, ready to be saved into your `README.md`.

Let me know if you also want me to scaffold the `.py` and `.sql` files referenced here.
