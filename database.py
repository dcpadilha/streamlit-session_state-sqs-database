import os

from dotenv import load_dotenv, find_dotenv
from sqlalchemy import create_engine, Column, String, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.schema import FetchedValue

load_dotenv(find_dotenv())

engine = create_engine('postgres://{}:{}@{}:{}/{}'.format(
    os.getenv('DATABASE_USER'),
    os.getenv('DATABASE_PASSWORD'),
    os.getenv('DATABASE_HOST'),
    os.getenv('DATABASE_PORT', 5432),
    os.getenv('DATABASE_DB_NAME')
))

base = declarative_base()


class AnnotationPets(base):
    __tablename__ = 'annotation_pets'
    filename = Column(String, primary_key=True)
    pet_type = Column(String)
    annotated_at = Column(TIMESTAMP, FetchedValue())


def insert_into_db(items):
    if not isinstance(items, list):
        items = [items]
    session_obj = sessionmaker(bind=engine)
    session = session_obj()
    for item in items:
        session.add(item)
    session.commit()


def update_db(table_obj: base, col_filter: dict, values: dict):
    session_obj = sessionmaker(bind=engine)
    session = session_obj()
    query = session.query(table_obj)
    for key, value in col_filter.items():
        query = query.filter(getattr(table_obj, key) == value)
    query.update(values)
    session.commit()
