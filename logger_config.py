import logging

# Configure the root logger
def configure_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Create console handler with a formatter
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)

# Configure the logger when this module is imported
configure_logger()

# Example of how to get a logger in other modules
def get_logger(name):
    return logging.getLogger(name)
