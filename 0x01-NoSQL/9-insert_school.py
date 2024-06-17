#!/usr/bin/env python3
"""Insert a document to a collection based on kwargs"""


def insert_school(mongo_collection, **kwargs):
    """Insert a document to a collection based on kwargs"""
    return mongo_collection.insert_one(kwargs).inserted_id
