#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker
"""
from functools import wraps
import redis
import requests
from typing import Callable, Union, Optional

cache = redis.Redis()


def get_cached_page(url: str) -> Optional[str]:
    """Get the HTML content of a particular URL from a cache.
    """
    html = cache.get(f"cache:{url}")
    if html is not None:
        return html.decode("utf-8")
    return None


def cache_page(expiration: int = 10) -> Callable[[Callable[[str], str]],
                                                 Callable[[str], str]]:
    """Cache the HTML content of a particular URL.
    """
    def page_counter(func: Callable[[str], str]) -> Callable[[str], str]:
        """Count the number of times a url has been visited.
        """
        @wraps(func)
        def wrapper(url: str) -> str:
            """Wrapper function for page_counter.
                Sets the number of times a url has been visited in a redis
                cache.
                The cache expires after 10 seconds.
            """
            cache.incr(f"count:{url}")
            html = get_cached_page(url)
            if html is not None:
                return html

            html = func(url)
            cache.setex(f"cache:{url}", expiration, html)

            return html
        return wrapper
    return page_counter


def get_count(url: str) -> int:
    """Get the number of times a URL has been visited.
    """
    return int(cache.get(f"count:{url}") or 0)


@cache_page(expiration=10)
def get_page(url: str) -> str:
    """Get the HTML content of a particular URL and return it.
    """
    html = requests.get(url)
    return html.text


if __name__ == "__main__":
    from time import sleep
    url = ("http://slowwly.robertomurray.co.uk/delay/"
           + "5000/url/https://www.google.com")
    print(get_count(url))
    for _ in range(5):
        get_page(url)
    print(get_count(url))
    print(get_cached_page(url))
    sleep(10)
    print(get_cached_page(url))
