from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

e = create_engine('sqlite:///tmp.db')
db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=e
))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from . import models
    Base.metadata.create_all(bind=e)