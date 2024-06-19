#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker
"""
from functools import wraps
import redis
import requests
from typing import Callable


def page_counter(func: Callable) -> Callable:
    """Count the number of times a url has been visited.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Wrapper function for page_counter.
            Sets the number of times a url has been visited in a redis cache.
            The cache expires after 10 seconds.
        """
        cache = redis.Redis()
        url = args[0]
        with cache.pipeline() as pipe:
            pipe.incr(f"count:{url}")
            pipe.expire(f"count:{url}", 10)
            pipe.execute()
        return func(*args, **kwargs)
    return wrapper


def get_count(url: str) -> int:
    """Get the number of times a URL has been visited.
    """
    cache = redis.Redis()
    return int(cache.get(f"count:{url}") or 0)


@page_counter
def get_page(url: str) -> str:
    """Get the HTML content of a particular URL and return it.
    """
    html = requests.get(url)
    return html.text


if __name__ == "__main__":
    from time import sleep
    url = ("http://slowwly.robertomurray.co.uk/delay/"
           + "5000/url/https://www.google.com")
    for _ in range(5):
        get_page(url)
    print(get_page(url))
    print(get_count(url))
    sleep(10)
    print(get_count(url))
