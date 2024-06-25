import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    log_format = '%(asctime)s %(levelname)s:%(message)s'
    log_directory = 'logs/SmartPrice.log'

    handler = RotatingFileHandler(log_directory, maxBytes=10*1024*1024, backupCount=10)
    handler.setFormatter(logging.Formatter(log_format))

    logging.basicConfig(level=logging.INFO, format=log_format, handlers=[handler])

setup_logging()
