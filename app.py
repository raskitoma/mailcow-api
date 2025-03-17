from flask import Flask, jsonify
import mysql.connector
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database Configuration from .env
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}

def get_user_data(username_email):
    """Fetch user data from mailcow_rc1users by username (email)."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query = "SELECT user_id, username, preferences FROM mailcow_rc1users WHERE username = %s"
        cursor.execute(query, (username_email,))
        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result  # Returns None if no record is found

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return None

@app.route('/2fa/mailcow/<string:username_email>', methods=['GET'])
def get_user(username_email):
    """API endpoint to fetch user data."""
    user_data = get_user_data(username_email)

    if user_data:
        return jsonify(user_data), 200
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(host=os.getenv("FLASK_RUN_HOST"), port=int(os.getenv("FLASK_RUN_PORT")), debug=os.getenv("FLASK_DEBUG") == "True")
