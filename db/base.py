#declarative base, metadata
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
#metadata for the database
from sqlalchemy import MetaData
metadata = MetaData()