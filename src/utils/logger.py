import logging
import colorlog

# Create a colorlog formatter
formatter = colorlog.ColoredFormatter(
    "%(log_color)s[%(asctime)s] - %(levelname)s: %(message)s",
    datefmt='%H:%M:%S',
    reset=True,
    log_colors={
        'INFO': 'blue',
        'ERROR': 'red',
    }
)

# Create a console handler and set its formatter
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Get a logger instance
logger = logging.getLogger()
logger.addHandler(console_handler)

# Set the logger's level
logger.setLevel(logging.INFO)


def log_info(message):
    logger.info(message)


def log_error(message):
    logger.error(message)
