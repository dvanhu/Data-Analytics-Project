# Install required packages
# Run these commands in your terminal or notebook before running the script
# pip install kaggle
# pip install pandas
# pip install sqlalchemy
# pip install pyodbc

import os
import json
import zipfile
import pandas as pd
import sqlite3

# Set Kaggle API credentials
kaggle_api = {
    "username": "YOUR_KAGGLE_USERNAME",
    "key": "YOUR_KAGGLE_API_KEY"
}

# Create the .kaggle directory in user's home if it doesn't exist
kaggle_dir = os.path.join(os.path.expanduser('~'), '.kaggle')
os.makedirs(kaggle_dir, exist_ok=True)

# Write Kaggle API key to kaggle.json file with proper permissions
kaggle_path = os.path.join(kaggle_dir, 'kaggle.json')
with open(kaggle_path, 'w') as f:
    json.dump(kaggle_api, f)
os.chmod(kaggle_path, 0o600)

print(f"Kaggle API key saved to: {kaggle_path}")


# Extract dataset from zip file downloaded via Kaggle API
zip_path = os.path.join(kaggle_dir, 'orders.csv.zip')
extract_to = os.path.join(os.getcwd(), 'retail_orders_data')
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to)

print(f"Dataset extracted to: {extract_to}")


# Load dataset into pandas DataFrame
csv_path = os.path.join(extract_to, 'orders.csv')
df = pd.read_csv(csv_path, na_values=['Not Available', 'unknown'])

# Display unique values in 'Ship Mode' column
print(df['Ship Mode'].unique())


# Clean column names: lowercase and replace spaces with underscores
df.columns = df.columns.str.lower().str.replace(' ', '_')

# Additional column renaming if necessary (example)
# df.rename(columns={'order_id': 'order_id', 'city': 'city'}, inplace=True)

# Display first 5 rows to verify changes
print(df.head(5))


# Derive new columns: discount, sale_price, and profit
df['discount'] = df['list_price'] * df['discount_percent'] * 0.01
df['sale_price'] = df['list_price'] - df['discount']
df['profit'] = df['sale_price'] - df['cost_price']

# Convert 'order_date' column to datetime
df['order_date'] = pd.to_datetime(df['order_date'], format="%Y-%m-%d")

# Drop unused columns to clean dataset
df.drop(columns=['list_price', 'cost_price', 'discount_percent'], inplace=True)

# Display updated DataFrame
print(df.head())


# Save DataFrame to SQLite database
conn = sqlite3.connect('mydatabase.db')

# Replace table if it exists, do not save DataFrame index
df.to_sql('orders', conn, if_exists='replace', index=False)

# Example SQL query: get distinct 'ship_mode' values
query = "SELECT DISTINCT ship_mode FROM orders;"
result = pd.read_sql_query(query, conn)
print(result)

# Close database connection
conn.close()
