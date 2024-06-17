#!/usr/bin/env python3
"""
Provides Nginx logs statistics stored in a MongoDB
"""
from pymongo import MongoClient


def log_stats():
    """
    Provides Nginx logs statistics stored in a MongoDB
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs = client.logs.nginx
    log_count = logs.count_documents({})
    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]

    print(f'{log_count} logs')
    print('Methods:')
    for method in methods:
        count = logs.count_documents({"method": method})
        print(f'\tmethod {method}: {count}')
    status_count = logs.count_documents({"method": "GET", "path": "/status"})
    print(f'{status_count} status check')


if __name__ == '__main__':
    log_stats()
