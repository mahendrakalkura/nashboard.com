# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy.schema import ThreadLocalMetaData

from settings import SQLALCHEMY

engine = create_engine(SQLALCHEMY, convert_unicode=True, echo=False, poolclass=NullPool, strategy='threadlocal')
base = declarative_base(bind=engine, metadata=ThreadLocalMetaData())
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=True))
