import logging
from docs_agent import __log_level__

# Custom filter -- we want to separate logs for stdout and stderr
class CustomLevelsFilter(logging.Filter):
    def __init__(self, low, high):
        super().__init__()
        self.low = low
        self.high = high
    
    def filter(self, record):
        return self.low <= record.levelno <= self.high

logger = logging.getLogger("docs_agent")

# Log error and higher to stderr
stderr_handler = logging.StreamHandler()
stderr_handler.setLevel(logging.WARNING)
stderr_handler.addFilter(CustomLevelsFilter(logging.WARNING, logging.CRITICAL))
stderr_handler.setFormatter(logging.Formatter('%(name)s: (%(levelname)s) %(message)s'))

# Log info and higher to stdout
stdout_handler = logging.StreamHandler()
stdout_handler.setLevel(logging.INFO)
stdout_handler.addFilter(CustomLevelsFilter(logging.INFO, logging.INFO))
stdout_handler.setFormatter(logging.Formatter('%(message)s'))

debug_handler = logging.StreamHandler()
debug_handler.setLevel(logging.DEBUG)
debug_handler.addFilter(CustomLevelsFilter(logging.DEBUG, logging.DEBUG))
debug_handler.setFormatter(logging.Formatter('%(name)s: (%(levelname)s) %(message)s'))

# Add handlers to logger
logger.addHandler(stderr_handler)
logger.addHandler(stdout_handler)
logger.addHandler(debug_handler)
logger.setLevel(getattr(logging, __log_level__.upper(), logging.DEBUG))