#!/usr/bin/env python3
"""0. Writing strings to Redis
    Module defines Cache class that will store instance of Redis client
"""
from functools import wraps
import redis
import uuid
from typing import Union, Callable, Optional, Any


def count_calls(method: Callable) -> Callable:
    """Decorator function that counts how many times a method of the Cache
    class is called
        Methods:
            wrapper(self, *args, **kwargs) -> Any: Wrapper function that counts
                how many times a method is called
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Wrapper function that counts how many times a function is called
            and returns the number of times it has been called
        """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator function that stores the history of inputs and outputs for a
    particular function
        Methods:
            wrapper(self, *args, **kwargs) -> Any: Wrapper function that stores
                the history of inputs and outputs for a particular function
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        """Wrapper function that stores the history of inputs and outputs for a
        particular function
        """
        self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(f"{method.__qualname__}:outputs", str(result))
        return result

    return wrapper


def replay(method: Callable) -> None:
    """Replay function to display history of calls of a praticular function
    eg. replay(cache.store)
    Cache.store was called 2 times:
    Cache.store(*[b'foo']) -> 'key1'
    Cache.store(*[123]) -> 'key2'
    """
    qualname = method.__qualname__
    cache = method.__self__
    count = cache._redis.get(qualname).decode('utf-8')
    print(f"{qualname} was called {count} times:")
    inputs = cache._redis.lrange(f"{qualname}:inputs", 0, -1)
    outputs = cache._redis.lrange(f"{qualname}:outputs", 0, -1)
    for i, o in zip(inputs, outputs):
        print(f"{qualname}(*{i.decode('utf-8')}) -> {o.decode('utf-8')}")


class Cache:
    """Cache class that will store instance of Redis client
        Methods:
            __init__(self)
            store(self, data: Union[str, bytes, int, float]) -> str
        Attributes:
            _redis: redis.client.Redis
    """
    def __init__(self) -> None:
        """Cache class constructor
            Initializes Redis client and flushes the existing database
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Method that stores input data in Redis
            Generates a random key, stores the input data in Redis using
            the key and returns the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str,
            fn: Optional[Callable[[bytes],
                                  Union[str, bytes,
                                        int,
                                        float]]] = None) -> Union[str,
                                                                  bytes, int,
                                                                  float, None]:
        """Method that retrieves data from Redis
            Retrieves the data stored in Redis using the key
            and returns the data
        """
        data = self._redis.get(key)
        if data is None:
            return None
        if fn is not None:
            return fn(data)
        return data

    def get_str(self, key: str) -> Optional[str]:
        """Method that retrieves string data from Redis
        """
        # return self.get(key, lambda data: data.decode('utf-8'))
        str_data = self.get(key, str)
        if isinstance(str_data, str):
            return str_data

    def get_int(self, key: str) -> Optional[int]:
        """Method that retrieves integer data from Redis
        """
        int_data = self.get(key, int)
        if isinstance(int_data, int):
            return int_data


if __name__ == "__main__":
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value
