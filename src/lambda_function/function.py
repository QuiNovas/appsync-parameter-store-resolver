import logging.config
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
	logger.info('Event :{}'.format(event))
	return event