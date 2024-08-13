#!/usr/bin/python3
import logging
# Advanced logging configuration
log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(filename='./logger/logs/movie_app.log', filemode='a', level=logging.INFO, format=log_format)
logging.getLogger('watchfiles').setLevel(logging.WARNING)
logger = logging.getLogger('movie_app')
