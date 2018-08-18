from util import create_logger

logger = create_logger('get_words', 'log.csv')

for word in ['first', 'second', 'third']:
    print(word)
    logger.debug('debug message')
    logger.warn('warn message')
    logger.critical('critical message')
