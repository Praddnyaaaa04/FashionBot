from flask import Flask, request, jsonify
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["FashionBot"]

# Function to search products by name
def search_product_by_name(product_name):
    results = db.products.find({"productDisplayName": {"$regex": product_name, "$options": "i"}})
    return list(results)

# Webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    
    # Extract the product name from the request
    product_name = req.get('queryResult').get('parameters').get('product_name')

    # Search for the product in the database
    found_products = search_product_by_name(product_name)
    
    # Prepare the response based on search results
    if found_products:
        product = found_products[0]
        response_text = f"Found {product['productDisplayName']} in the {product['masterCategory']} category."
    else:
        response_text = "Sorry, I couldn't find the product you're looking for."

    # Return the response to Dialogflow
    return jsonify({
        "fulfillmentText": response_text
    })

if __name__ == '__main__':
    app.run(port=5000, debug=True)
