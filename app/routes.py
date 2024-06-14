from flask import request, jsonify, session, current_app as app
from app import app
from app.database import create_user, get_user_by_email

@app.route('/')
def home():
    return "Hello World"

@app.route('/register', methods=['POST'])
def register():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    if get_user_by_email(email):
        return jsonify({'message': 'Email address already registered'}), 400

    create_user(email, password)

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    user = get_user_by_email(email)

    if user is None or not user.check_password(password):
        return jsonify({'message': 'Invalid email or password'}), 401

    # Log in the user (for session-based authentication)
    session['user_id'] = user.id

    return jsonify({'message': 'Logged in successfully'}), 200

@app.route('/logout', methods=['POST'])
def logout():
    if 'user_id' not in session:
        return jsonify({'message': 'User already logged out'}), 200

    # Clear the session data
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200
