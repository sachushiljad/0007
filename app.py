from flask import Flask, jsonify
from sqlalchemy import create_engine, text
import logging
import os
from urllib.parse import urlparse

app = Flask(__name__)

# Database connection string (e.g., stored in environment variable)
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@host:5432/database')

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL)

@app.route('/', methods=['GET'])
def root():
    try:
        # Parse the connection string for debugging (excluding password)
        parsed = urlparse(DATABASE_URL)
        logging.info('--- Database Connection Details ---')
        logging.info(f"Host: {parsed.hostname}")
        logging.info(f"Database: {parsed.path.lstrip('/')}")
        logging.info(f"Username: {parsed.username}")
        logging.info(f"Port: {parsed.port}")
        logging.info(f"Dialect: {parsed.scheme}")
        logging.info('----------------------------------')

        # Query current time
        with engine.connect() as connection:
            result = connection.execute(text("SELECT NOW() AS current_time"))
            current_time = result.scalar()

        return jsonify({
            "message": "API is working!",
            "current_time": str(current_time)
        }), 200
    except Exception as e:
        logging.error(f"Error fetching time from DB: {e}")
        return jsonify({"error": "Failed to get time from database"}), 500

if __name__ == "__main__":
    app.run(debug=True)
