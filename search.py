import pandas as pd
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["FashionBot"]

# Load CSV file with error handling
file_path = "E:\RBL\Search_by_product\Product-trail.csv"  # Ensure this is the correct file path
products_df = pd.read_csv(file_path, on_bad_lines='skip')

# Fill NaN values with an empty string
products_df = products_df.fillna('')

# Insert products into MongoDB
for _, row in products_df.iterrows():
    product_data = {
        "id": row['id'],
        "gender": row['gender'],
        "masterCategory": row['masterCategory'],
        "subCategory": row['subCategory'],
        "articleType": row['articleType'].split(', ') if isinstance(row['articleType'], str) else [],
        "baseColour": row['baseColour'].split(', ') if isinstance(row['baseColour'], str) else [],
        "season": row['season'].split(', ') if isinstance(row['season'], str) else [],
        "usage": row['usage'].split(', ') if isinstance(row['usage'], str) else [],
        "productDisplayName": row['productDisplayName'].split(', ') if isinstance(row['productDisplayName'], str) else [],
    }
    db.products.insert_one(product_data)
