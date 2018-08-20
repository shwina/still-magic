import sys
import logging

# Create logger.
logger = logging.getLogger('example')
logger.setLevel(logging.DEBUG)

# Define common format.
formatter = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(message)s',
                              datefmt='%Y-%m-%dT%H:%M:%S')

# Send all logging messages to a file.
toFile = logging.FileHandler('log.csv')
toFile.setLevel(logging.DEBUG)
toFile.setFormatter(formatter)

# Send errors and critical messages to standard error.
toScreen = logging.StreamHandler(sys.stderr)
toScreen.setLevel(logging.ERROR)
toScreen.setFormatter(formatter)

# Stitch everything together.
logger.addHandler(toFile)
logger.addHandler(toScreen)

# Try some messages.
logger.debug('debug')
logger.info('info')
logger.warning('warning')
logger.error('error')
logger.critical('critical')
