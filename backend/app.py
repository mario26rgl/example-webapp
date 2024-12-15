from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import time

app = Flask(__name__)

# Enabling Cross-Origin Resource Sharing (CORS)
CORS(app)

# Database connection configuration
db_config = {
    'host': 'db-svc.database.svc.cluster.local',
    'user': 'root',
    'password': 'P@ssword!1234',
    'database': 'example_webapp_db',
    'port': 3306  # Default MySQL port
}

# Function to initialize the database connection
def get_db_connection():
    connection = mysql.connector.connect(**db_config)
    return connection

def startup_checks():
    retries = 5
    while retries > 0:
        try:
            connection = get_db_connection()
            # Create the table if it does not exist
            cursor = connection.cursor()
            cursor.execute("USE example_webapp_db")
            cursor.execute("CREATE TABLE IF NOT EXISTS items (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), description TEXT)")
            cursor.close()
            connection.close()
            break
        except mysql.connector.Error:
            retries -= 1
            time.sleep(2)
    else:
        raise Exception("ERROR! Failed to connect to the database")

# Home route
@app.route("/")
def home():
    return "Welcome to the Backend API connected to MySQL!"

# Read all data
@app.route("/api/data", methods=["GET"])
def get_data():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items")
    data = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify(data), 200

# Create new data
@app.route("/api/data", methods=["POST"])
def create_data():
    new_item = request.get_json()
    name = new_item.get("name")
    description = new_item.get("description")

    if not name or not description:
        return jsonify({"message": "Invalid input"}), 400

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO items (name, description) VALUES (%s, %s)", (name, description))
    connection.commit()
    new_id = cursor.lastrowid
    cursor.close()
    connection.close()

    return jsonify({"message": "Item added", "id": new_id}), 201

# Update an existing data item
@app.route("/api/data/<int:item_id>", methods=["PUT"])
def update_data(item_id):
    updated_item = request.get_json()
    name = updated_item.get("name")
    description = updated_item.get("description")

    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("UPDATE items SET name = %s, description = %s WHERE id = %s", (name, description, item_id))
    connection.commit()
    cursor.close()
    connection.close()

    if cursor.rowcount == 0:
        return jsonify({"message": "Item not found"}), 404

    return jsonify({"message": "Item updated"}), 200

# Delete a data item
@app.route("/api/data/<int:item_id>", methods=["DELETE"])
def delete_data(item_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM items WHERE id = %s", (item_id,))
    connection.commit()
    cursor.close()
    connection.close()

    if cursor.rowcount == 0:
        return jsonify({"message": "Item not found"}), 404

    return jsonify({"message": "Item deleted"}), 200

if __name__ == "__main__":
    startup_checks()
    app.run(host="0.0.0.0", port=80, debug=True)