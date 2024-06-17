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
    method = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    aggregate_methods = logs.aggregate([
        {'$project': {
            'method': 1,
            '_id': 0,
            },
         },
        {'$match': {
            'method': {'$in': method},
            },
         },
        {'$group': {
            '_id': '$method',
            'count': {'$sum': 1},
            },
         },
        {'$sort': {'count': -1}},
    ])

    aggregate_status = logs.aggregate([
        {'$project': {
            'method': 1,
            '_id': 0,
            'path': 1,
            },
         },
        {'$match': {
            'method': 'GET',
            'path': '/status',
            },
         },
        {'$count': 'status'},
        {'$limit': 1},
    ]).next()

    print(f'{log_count} logs')
    print('Methods:')
    for item in aggregate_methods:
        print(f'\tmethod {item.get("_id")}: {item.get("count")}')
        method.remove(item.get("_id"))
    for item in sorted(method, reverse=True):
        print(f'\tmethod {item}: 0')
    print(f'{aggregate_status.get("status")} status check')


if __name__ == '__main__':
    log_stats()
