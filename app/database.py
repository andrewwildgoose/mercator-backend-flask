import os
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Load environment variables from .env file
load_dotenv()

# Initialize SQLAlchemy object
db = SQLAlchemy()

def init_db(app):
    # Configure SQLAlchemy settings
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    
    # Initialize SQLAlchemy with the Flask app
    db.init_app(app)

    # Create all tables based on the defined models
    with app.app_context():
        db.create_all()

def create_user(email, password, name):
    from app.models import User  # Import here to avoid circular import
    hashed_password = generate_password_hash(password)
    new_user = User(email=email, password_hash=hashed_password, name=name)
    db.session.add(new_user)
    db.session.commit()

def get_user_by_email(email):
    from app.models import User  # Import here to avoid circular import
    return User.query.filter_by(email=email).first()
