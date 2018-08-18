import sys
from util import create_logger

logger = create_logger('count_words', 'log.csv')

count = 0
for line in sys.stdin:
    count += 1
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
print(count)
