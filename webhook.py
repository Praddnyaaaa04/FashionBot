from flask import Flask, request, jsonify
from pymongo import MongoClient, errors
import os

app = Flask(__name__)

# Initialize MongoDB client
try:
    # Use environment variable for MongoDB connection string
    client = MongoClient(os.getenv('MONGODB_CONNECTION_STRING', 'mongodb://localhost:27017/'))
    db = client['FashionBot']
    collection = db['SearchProduct']
except errors.ConnectionError as e:
    print(f"Failed to connect to MongoDB: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        query_text = data.get('queryResult', {}).get('queryText', '')

        # Check if query contains the keyword for T-shirts
        if 'show me a t-shirt' in query_text.lower():
            # Query MongoDB for products matching the query
            products = collection.find({"category": "t-shirt"})
            product_list = [{"name": product.get("name", "Unknown"), "price": product.get("price", "Unknown")} for product in products]

            if product_list:
                response_text = "Here are some T-shirts you might like:\n"
                for product in product_list:
                    response_text += f"- {product['name']} (${product['price']})\n"
            else:
                response_text = "No T-shirts found."

            return jsonify({"fulfillmentText": response_text})
        else:
            return jsonify({"fulfillmentText": "Sorry, I didn't understand that."})
    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"fulfillmentText": "An error occurred while processing your request."})

if __name__ == '__main__':
    app.run(debug=True)
