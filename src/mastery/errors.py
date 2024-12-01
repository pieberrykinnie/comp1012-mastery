from flask import jsonify
from werkzeug.exceptions import HTTPException
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('mastery.log')
    ]
)
logger = logging.getLogger(__name__)


class MasteryError(Exception):
    """Base exception class for mastery system"""

    def __init__(self, message, status_code=400):
        super().__init__()
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        return {'error': self.message}


def handle_error(error):
    """Generic error handler for all exceptions"""
    if isinstance(error, MasteryError):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        logger.error(f"MasteryError: {error.message}")
    elif isinstance(error, HTTPException):
        response = jsonify({'error': error.description})
        response.status_code = error.code
        logger.error(f"HTTPException: {error.description}")
    else:
        response = jsonify({'error': 'An unexpected error occurred'})
        response.status_code = 500
        logger.error(f"Unexpected error: {str(error)}", exc_info=True)

    return response
