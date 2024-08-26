import logging
from functools import wraps

logger = logging.getLogger(__name__)

def log_function_call(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Starting {func.__name__}", extra={'function': func.__name__})
        try:
            result = func(*args, **kwargs)
            logger.info(f"Finished {func.__name__}", extra={'function': func.__name__})
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}", extra={'function': func.__name__, 'exception': str(e)})
            raise
    return wrapper