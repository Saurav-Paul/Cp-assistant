import logging
from settings.settings import DEBUG

logger = logging.getLogger()

if DEBUG:
    logger.setLevel(20)
