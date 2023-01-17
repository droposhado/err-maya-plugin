"""Configuration file to pytest tests"""
from sqlalchemy import text

from model import engine


def pytest_runtest_setup(item):
    """Cleanup tables before start a new test"""

    sql = text("""CREATE TABLE IF NOT EXISTS
  public.liquids (
    id uuid NOT NULL DEFAULT uuid_generate_v4(),
    client_name character varying NULL,
    client_version character varying NULL,
    creation_date timestamp without time zone NULL,
    last_modification timestamp without time zone NULL,
    quantity integer NULL,
    unit character varying NULL,
    type character varying NULL,
    username character varying NULL
  );

ALTER TABLE
  public.liquids
ADD
  CONSTRAINT liquids_pkey PRIMARY KEY (id);""")
    results = engine.execute(sql)


    sql = text('TRUNCATE liquids;')
    results = engine.execute(sql)

    print(results)
