#!/usr/bin/env python3
"""
method that returns the list of school students
sorted by average score
"""


def top_students(mongo_collection):
    """
    method that returns the list of school students
    sorted by average score
    """
    return mongo_collection.aggregate([
        {'$project': {
            'name': '$name',
            'averageScore': {'$avg': '$topics.score'}
        }},
        {'$sort': {'averageScore': -1}}
    ])
