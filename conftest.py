"""Configuration file to pytest tests"""
from sqlalchemy import text

from model import engine


def pytest_runtest_setup(item):
    """Cleanup tables before start a new test"""

    sql = text('TRUNCATE liquids;')
    results = engine.execute(sql)

    print(results)
