from flask import Flask, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

# Initialize MongoDB client
client = MongoClient("mongodb://localhost:27017/")
db = client['FashionBot']
collection = db['SearchProduct']

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    query_text = data.get('queryResult', {}).get('queryText', '')

    # Example query logic
    if 'show me a t-shirt' in query_text.lower():
        # Query MongoDB for products matching the query
        products = collection.find({"category": "t-shirt"})
        product_list = [{"name": product["name"], "price": product["price"]} for product in products]
        
        if product_list:
            response_text = "Here are some T-shirts you might like:\n"
            for product in product_list:
                response_text += f"- {product['name']} (${product['price']})\n"
        else:
            response_text = "No T-shirts found."

        return jsonify({"fulfillmentText": response_text})
    else:
        return jsonify({"fulfillmentText": "Sorry, I didn't understand that."})

if __name__ == '__main__':
    app.run(debug=True)
