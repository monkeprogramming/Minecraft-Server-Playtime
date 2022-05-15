import logging
from os import getenv

log_level = logging.getLevelName(getenv('LOG_LEVEL') or 'DEBUG')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger = logging.getLogger('playtime')
logger.addHandler(stream_handler)

logger.setLevel(log_level)
