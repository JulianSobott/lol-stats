from riotwatcher import ApiError
import time
from sentry_sdk import capture_exception


def call_with_retry(max_retries: int):
    def decorate(f):
        def applicator(*args, **kwargs):
            retry = 0
            while retry+1 <= max_retries:
                retry += 1
                try:
                    return f(*args, **kwargs)
                except ApiError as e:
                    capture_exception(e)
                    print('API Error trying to retrieve summoner data: ', e)
                    print(f'Retrying in 5s (Retry {retry}/{max_retries})')
                    time.sleep(5)
        return applicator
    return decorate
