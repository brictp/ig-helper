# logger_config.py
import os
import logging

# Logger config
log_directory = "./logs"
os.makedirs(log_directory, exist_ok=True)  # Create logs folder if not exists
log_file = os.path.join(log_directory, "app.log")

logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,  # Logging errors
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def log_error(error_message):
    """
    Function to register errors in the log file.
    """
    logging.error(error_message)
