import os
from pathlib import Path

class Config:
    """Basic configuration"""
    # Get the project root
    PROJECT_ROOT = Path(__file__).parent.parent

    # Database
    DATABASE_DIR = PROJECT_ROOT / 'database'
    DATABASE_NAME = 'fastaflow.db'
    SQLALCHEMY_DATABASE_URI = f'sqlite:///{DATABASE_DIR / DATABASE_NAME}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File uploads
    UPLOAD_DIR = PROJECT_ROOT / 'temp'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'fasta', 'fas', 'fa', 'fna', 'ffn', 'faa', 'mpfa', 'frn'}

    # Security
    SECRET_KEY = 'z\x16_\x0f\xe2N\xdd\x83^\x07!<'  # In production, load from environment


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_ECHO = True  # Log SQL queries


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False

    # In production, load secret key from environment
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', Config.SECRET_KEY)

    # Use environment variable for database in production
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        Config.SQLALCHEMY_DATABASE_URI
    )