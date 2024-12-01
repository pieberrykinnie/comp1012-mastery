from datetime import timedelta
from flask import Flask, request, jsonify
from flask_login import LoginManager
from .auth import auth_bp, login_manager
from .models import db
from .repository import ProblemRepository
from .tracker import ProgressTracker
import os


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY='dev',
            SQLALCHEMY_DATABASE_URI='sqlite:///mastery.db',
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            PERMANENT_SESSION_LIFETIME=timedelta(
                days=7)  # Session expires in 7 days
        )
    else:
        app.config.update(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    repo = ProblemRepository()
    tracker = ProgressTracker()

    @app.route('/api/problems/<topic>', methods=['GET'])
    def get_problems(topic):
        try:
            problems = repo.get_problems_by_topic(topic)
            return jsonify([{
                'id': p.id,
                'topic': p.topic,
                'difficulty': p.difficulty,
                'description': p.description
            } for p in problems])
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/api/problems/<int:problem_id>', methods=['GET'])
    def get_problem(problem_id):
        try:
            problem = repo.get_problem_by_id(problem_id)
            if not problem:
                return jsonify({'error': 'Problem not found'}), 404
            return jsonify({
                'id': problem.id,
                'topic': problem.topic,
                'difficulty': problem.difficulty,
                'description': problem.description,
                'starter_code': problem.starter_code
            })
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/api/submit/<int:problem_id>', methods=['POST'])
    def submit_solution(problem_id):
        try:
            data = request.get_json()
            if not data or 'code' not in data or 'user_id' not in data:
                return jsonify({'error': 'Missing required fields'}), 400

            result = tracker.record_attempt(
                data['user_id'],
                problem_id,
                data['code']
            )
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    # Initialize Flask-Login
    login_manager.init_app(app)
    app.config['SECRET_KEY'] = os.getenv(
        'SECRET_KEY', 'dev-key-change-in-prod')

    # Register blueprints only if not already registered
    if 'auth' not in app.blueprints:
        app.register_blueprint(auth_bp, url_prefix='/auth')

    return app
