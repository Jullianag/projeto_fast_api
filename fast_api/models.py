from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime


CONN = f'sqlite:///fastapibanco.db'

engine = create_engine(CONN, echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Pessoas(Base):
    __tablename__ = 'Pessoas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(50))
    usuario = Column(String(20))
    senha = Column(String(10))


class Tokens(Base):
    __tablename__ = 'Tokens'
    id = Column(Integer, primary_key=True)
    id_pessoa = Column(Integer, ForeignKey('Pessoas.id'))
    token = Column(String(100))
    data = Column(DateTime, default=datetime.datetime.utcnow())


Base.metadata.create_all(engine)
