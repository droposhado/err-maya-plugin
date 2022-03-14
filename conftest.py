"""Configuration file to pytest tests"""
import os

from pymongo import MongoClient

ERR_MAYA_MONGODB_URL = os.getenv(
        'ERR_MAYA_MONGODB_URL',
        'mongodb://localhost/test?retryWrites=true&w=majority')


def pytest_runtest_setup(item):
    """Drop collection before start a new test"""
    mongo_client = MongoClient(ERR_MAYA_MONGODB_URL)
    database = mongo_client.test
    print(item)
    print(database.coffee.drop())
    print(database.water.drop())
