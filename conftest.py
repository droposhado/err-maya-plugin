"""Configuration file to pytest tests"""
import datetime
import os
import uuid

from errbot import BotPlugin, botcmd
from sqlalchemy import Column, DateTime, Integer, String, create_engine, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

ERR_MAYA_DATABASE_URL = os.getenv('ERR_MAYA_DATABASE_URL',
                                  'postgresql://maya:maya@localhost:5432/maya')


class LiquidModel(Base):
    """Represent database model liquid"""

    __tablename__ = 'liquids'

    id = Column(UUID(as_uuid=True),
                primary_key=True,
                unique=True,
                server_default=text("uuid_generate_v4()"),)

    client_name = Column(String)
    client_version = Column(String)
    creation_date = Column(DateTime)
    last_modification = Column(DateTime)
    quantity = Column(Integer)
    unit = Column(String)
    type = Column(String)
    username = Column(String)


def pytest_runtest_setup(item):
    """Cleanup tables before start a new test"""

    engine = create_engine(ERR_MAYA_DATABASE_URL)
    sql = text('TRUNCATE liquids;')
    results = engine.execute(sql)

    print(results)
