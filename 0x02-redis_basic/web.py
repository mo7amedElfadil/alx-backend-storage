#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker
"""
from functools import wraps
import redis
import requests
from typing import Callable

cache = redis.Redis()


def page_counter(func: Callable) -> Callable:
    """Count the number of times a url has been visited.
    """
    @wraps(func)
    def wrapper(url) -> str:
        """Wrapper function for page_counter.
            Sets the number of times a url has been visited in a redis cache.
            The cache expires after 10 seconds.
        """
        cache.incr(f"count:{url}")
        html = cache.get(f"cache:{url}")
        if html:
            return html.decode("utf-8")
        html = func(url)
        cache.set(f"count:{url}", 0)
        cache.setex(f"cache:{url}", 10, html)
        return html
    return wrapper


@page_counter
def get_page(url: str) -> str:
    """Get the HTML content of a particular URL and return it.
    """
    html = requests.get(url)
    return html.text
