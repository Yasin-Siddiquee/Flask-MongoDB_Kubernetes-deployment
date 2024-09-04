from flask import Flask, request, jsonify # Import necessary modules from Flask
from pymongo import MongoClient # Import MongoClient to interact with MongoDB
from datetime import datetime # Import datetime to get the current time
import os # Import os to access environment variables
# Initialize the Flask application
app = Flask(__name__)
# Set up the MongoDB client
# The MongoDB URI is fetched from the environment variable 'MONGODB_URI'
# If not found, it defaults to 'mongodb://localhost:27017/'
client = MongoClient(os.environ.get("MONGODB_URI", "mongodb://localhost:27017/"))
# Connect to the database named 'flask_db'
db = client.flask_db
# Connect to the collection named 'data' within the 'flask_db' database
collection = db.data
# Define the route for the root URL
@app.route('/')
def index():
# Return a welcome message with the current time
    return f"Welcome to the Flask app! The current time is: {datetime.now()}"
# Define the route for the '/data' endpoint
# This endpoint supports both GET and POST methods
@app.route('/data', methods=['GET', 'POST'])
def data():
    if request.method == 'POST':
        # If the request method is POST, get the JSON data from the request
        data = request.get_json()
        # Insert the data into the 'data' collection in MongoDB
        collection.insert_one(data)
        # Return a success message with status code 201 (Created)
        return jsonify({"status": "Data inserted"}), 201
    elif request.method == 'GET':
        # If the request method is GET, retrieve all documents from the 'data' collection
        # Convert the documents to a list, excluding the '_id' field
        data = list(collection.find({}, {"_id": 0}))
        # Return the data as a JSON response with status code 200 (OK)
        return jsonify(data), 200
# Run the Flask application
# The application will listen on all available IP addresses (0.0.0.0) and port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)