from flask import Blueprint, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from .models.user import User
from .models import db

auth_bp = Blueprint('auth', __name__)
login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@auth_bp.route('/register', methods=['POST'])
def register():
    if current_user.is_authenticated:
        return jsonify({'error': 'Already logged in'}), 400

    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400

    user = User(username=data['username'])
    user.set_password(data['password'])

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Registration failed'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({'message': 'Already logged in'}), 200

    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        return jsonify({'message': 'Logged in successfully'}), 200

    return jsonify({'error': 'Invalid username or password'}), 401


@auth_bp.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify({'message': 'Logged out successfully'}), 200
    return jsonify({'error': 'Not logged in'}), 401
