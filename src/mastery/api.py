from flask import Flask, request, jsonify
from .models import db
from .repository import ProblemRepository
from .tracker import ProgressTracker
import os


def create_app(test_config=None):
    app = Flask(__name__)

    if test_config is None:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'DATABASE_URL', 'sqlite:///mastery.db'
        )
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

    return app
