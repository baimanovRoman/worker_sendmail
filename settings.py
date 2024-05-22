import os

from peewee import PostgresqlDatabase
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

APP_NAME = "worker_rabbitmq"

if os.getenv("INTEGRATION_TEST", False):
    POSTGRES_DB = 'test_' + os.getenv("POSTGRES_DB")
    LOGGING_DIR_PATH = Path(BASE_DIR.parent, "integration_tests", "logs", APP_NAME)
    RABBITMQ_MAIL_MESSAGE_QUEUE = os.getenv("TEST_RABBITMQ_MAIL_MESSAGE_QUEUE", "test_message")
    LOG_LEVEL = os.getenv("TEST_LOG_LEVEL", "INFO")
else:
    POSTGRES_DB = os.getenv("POSTGRES_DB")
    LOGGING_DIR_PATH = Path(BASE_DIR.parent, "logs", APP_NAME)
    RABBITMQ_MAIL_MESSAGE_QUEUE = os.getenv("RABBITMQ_MAIL_MESSAGE_QUEUE", "message")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT_SSL = os.getenv("EMAIL_PORT_SSL")
EMAIL_PORT_TLS = os.getenv("EMAIL_PORT_TLS")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "127.0.0.1")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5672")

ERROR_COOLDOWN = 10 #sec

db = PostgresqlDatabase(
    POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}]; [{levelname}]; message={message}; module={module}; name={name}; process={process:d}; thread={thread:d}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "[{asctime}]; [{levelname}]; message={message}; module={module}; name={name}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "stream": "ext://sys.stdout",
        },
        "file_debug": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024*1024*5, # 5 MB
            "backupCount": 5,
            "formatter": "simple",
            "filename": Path(LOGGING_DIR_PATH, "debug.log"),
        },
        "file_info": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024*1024*5, # 5 MB
            "backupCount": 5,
            "formatter": "simple",
            "filename": Path(LOGGING_DIR_PATH, "info.log"),
        },
        "file_warning": {
            "level": "WARNING",
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024*1024*5, # 5 MB
            "backupCount": 5,
            "formatter": "simple",
            "filename": Path(LOGGING_DIR_PATH, "warning.log"),
        },
        "file_error": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024*1024*5, # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
            "filename": Path(LOGGING_DIR_PATH, "error.log"),
        },
        "file_critical": {
            "level": "CRITICAL",
            "class": "logging.handlers.RotatingFileHandler",
            "maxBytes": 1024*1024*5, # 5 MB
            "backupCount": 5,
            "formatter": "verbose",
            "filename": Path(LOGGING_DIR_PATH, "critical.log"),
        },
    },
    "loggers": {
        "": {
            "handlers": [
                "console",
                "file_debug", 
                "file_info", 
                "file_warning", 
                "file_error", 
                "file_critical"
            ],
            "level": LOG_LEVEL
        }
    }
}

LOG_AVAILABLE_LEVELS = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

