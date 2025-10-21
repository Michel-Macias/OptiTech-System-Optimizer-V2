# src/logger.py

import logging
import logging.handlers
import os
from src import config_manager

APP_LOGGER_NAME = 'OptiTechOptimizer'

def setup_logging(log_file=None, console_level=logging.INFO, file_level=logging.DEBUG, max_bytes=10*1024*1024, backup_count=5):
    """Configures the application-wide logger.

    Args:
        log_file (str, optional): Path to the log file. Defaults to config_manager's log path.
        console_level (int, optional): Logging level for console output. Defaults to INFO.
        file_level (int, optional): Logging level for file output. Defaults to DEBUG.
        max_bytes (int, optional): Maximum size of a log file before rotation. Defaults to 10MB.
        backup_count (int, optional): Number of backup log files to keep. Defaults to 5.
    """
    # Ensure config_manager is initialized and paths are available
    if log_file is None:
        log_file = os.path.join(config_manager.get_log_path(), "app.log")

    # Create log directory if it doesn't exist
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Get the root logger for the application
    app_logger = logging.getLogger(APP_LOGGER_NAME)
    app_logger.setLevel(file_level) # Set overall level to the lowest (DEBUG) to capture all messages

    # Define a common formatter for both console and file handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S,%f'
    )

    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)
    app_logger.addHandler(console_handler)

    # File Handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding=config_manager.get_default_encoding()
    )
    file_handler.setLevel(file_level)
    file_handler.setFormatter(formatter)
    app_logger.addHandler(file_handler)

    # Prevent messages from being propagated to the root logger
    app_logger.propagate = False

# Initialize logging when the module is imported
setup_logging()
