import click
import json
from flask import current_app
from .models import db
from .repository import ProblemRepository
from .analytics import ProgressAnalytics
from .recommender import ProblemRecommender
from .reports import ReportGenerator
from .feedback import FeedbackGenerator


@click.group()
def cli():
    """COMP 1012 Mastery Learning System CLI"""
    pass


@cli.command()
@click.option('--topic', required=True, help='Topic identifier (e.g., BASICS)')
@click.option('--difficulty', default=1, help='Problem difficulty (1-5)')
def add_problem(topic, difficulty):
    """Add a new practice problem"""
    with current_app.app_context():
        repo = ProblemRepository()
        problem = repo.create_problem(topic, difficulty)
        click.echo(
            f"Created problem {problem.id} for {topic} (difficulty: {difficulty})")


@cli.command()
@click.argument('user_id')
def show_progress(user_id):
    """Show progress for a specific user"""
    with current_app.app_context():
        analytics = ProgressAnalytics()
        stats = analytics.get_user_stats(user_id)
        click.echo(json.dumps(stats, indent=2))


@cli.command()
@click.argument('user_id')
def get_recommendations(user_id):
    """Get problem recommendations for a user"""
    with current_app.app_context():
        recommender = ProblemRecommender()
        recommendations = recommender.get_recommendations(user_id)
        click.echo(json.dumps(recommendations, indent=2))


@cli.command()
@click.argument('user_id')
def generate_report(user_id):
    """Generate a detailed progress report"""
    with current_app.app_context():
        generator = ReportGenerator()
        report = generator.generate_student_report(user_id)
        click.echo(json.dumps(report, indent=2))


@cli.command()
@click.argument('user_id')
def get_feedback(user_id):
    """Get personalized feedback"""
    with current_app.app_context():
        generator = FeedbackGenerator()
        feedback = generator.generate_feedback(user_id)
        click.echo(json.dumps(feedback, indent=2))


@cli.command()
def init_db():
    """Initialize the database"""
    with current_app.app_context():
        db.create_all()
        click.echo("Database initialized")
