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
    def wrapper(*args, **kwargs) -> str:
        """Wrapper function for page_counter.
            Sets the number of times a url has been visited in a redis cache.
            The cache expires after 10 seconds.
        """
        url = args[0]
        cache.incr(f"count:{url}")
        html = cache.get(f"cache:{url}")
        if html:
            return html.decode("utf-8")
        html = func(*args, **kwargs)
        cache.set(f"count:{url}", 0)
        cache.setex(f"cache:{url}", 10, html)
        return html
    return wrapper


def get_count(url: str) -> int:
    """Get the number of times a URL has been visited.
    """
    cache = redis.Redis()
    return int(cache.get(f"count:{url}") or 0)


def get_cached_page(url: str) -> str:
    """Get the HTML content of a particular URL from a cache.
    """
    cache = redis.Redis()
    html = cache.get(f"cache:{url}")
    if html:
        return html.decode("utf-8")
    return "No cache available."


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
    print(get_count(url))
    print(get_cached_page(url))
    sleep(10)
    print(get_cached_page(url))
