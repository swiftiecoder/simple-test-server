from flask import Flask, request, jsonify
# from dotenv import load_dotenv
from pymongo import MongoClient
import os

# # Load environment variables from .env file
# load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize MongoDB connection
mongo_client = MongoClient(os.getenv('MONGO_URI'))
db = mongo_client['langchain-db']  # Replace with your database name
collection = db['traces']  # Replace with your collection name

# Variable to store the payload of the last POST request
last_payload = None

@app.route('/api', methods=['POST'])
def api():
    global last_payload
    # Get JSON payload from the request
    last_payload = request.get_json()

    # Ensure payload contains recipient and message
    if not last_payload or 'recipient' not in last_payload or 'message' not in last_payload:
        return jsonify({"error": "Payload must include 'recipient' and 'message'"}), 400

    recipient = last_payload['recipient']
    message = last_payload['message']

    # Add the data to the MongoDB collection
    collection.update_one(
        {"recipient": recipient},  # Query by recipient
        {"$push": {"message": message}},  # Update message
        upsert=True  # Insert if not exists
    )

    return jsonify({"message": "Payload received and stored"}), 200

@app.route('/')
def index():
    if last_payload is None:
        return jsonify({"message": "No POST requests received yet."}), 200
    return jsonify(last_payload), 200

if __name__ == '__main__':
    app.run()