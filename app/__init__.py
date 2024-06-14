import os
from flask import Flask
from dotenv import load_dotenv
from app.database import init_db, db
from flask_migrate import Migrate

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure Flask app
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Set secret key for session management

# Initialize Flask-Migrate with the Flask app and SQLAlchemy db instance
migrate = Migrate(app, db)

# Initialize the database using the function from database.py
init_db(app)

# Import routes after app is created to avoid circular imports
from app import routes