import logging
import os
from logging.handlers import RotatingFileHandler
from datetime import datetime


# create logs dir if doesn't exist
logs_path = os.path.join(os.getcwd(), 'logs')
os.makedirs(logs_path, exist_ok=True)

# create log filename with timestamp
LOG_FILE_NAME = f"{datetime.now().strftime('%d_%m_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE_NAME)

# logging.basicConfig(
#     filename=LOG_FILE_PATH,
#     format="[ %(asctime)s ] - %(levelname)s - %(message)s",
#     level=logging.INFO
# )

# define logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

file_formatter = logging.Formatter("[ %(asctime)s ] - %(levelname)s - %(message)s")
console_formatter = logging.Formatter("%(message)s")

# define handlers
file_handler = logging.FileHandler(LOG_FILE_PATH)
file_handler.setFormatter(file_formatter)

console_handler = logging.StreamHandler()
console_handler.setFormatter(console_formatter)

# add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)