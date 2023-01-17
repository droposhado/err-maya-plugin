"""Configuration file to pytest tests"""
from model import engine
from sqlalchemy import text


def pytest_runtest_setup(item):
    """Cleanup tables before start a new test"""

    sql = text('TRUNCATE liquids;')
    results = engine.execute(sql)

    print(results)
