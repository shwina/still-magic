import logging

def create_logger(application, filename):

    # Create logger.
    logger = logging.getLogger(application)
    logger.setLevel(logging.WARNING)

    # Send messages to standard output.
    handler = logging.FileHandler(filename)
    handler.setLevel(logging.DEBUG)

    # Define format.
    formatter = logging.Formatter('%(asctime)s,%(name)s,%(levelname)s,%(message)s',
                                  datefmt='%Y-%m-%dT%H:%M:%S')

    # Stitch everything together.
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
