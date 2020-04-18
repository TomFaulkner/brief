import logging
from datetime import datetime, timedelta
from functools import wraps

logger = logging.getLogger(__name__)


class ATimedMemo:
    def __init__(self, minutes=10, seconds=0):
        if not minutes:
            minutes = 0
        self.time_addition = minutes * 60 + seconds
        self.last_run = None

    def __call__(self, func, *args, **kwargs):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not self.last_run or datetime.now() > self.last_run + timedelta(
                seconds=self.time_addition
            ):
                logger.debug(f"No cache, running function, {func.__name__}.")
                self.last_run = datetime.now()
                self.cache = await func(*args, **kwargs)
            else:
                logger.debug("Returning cached results.")
            return self.cache

        return wrapper
