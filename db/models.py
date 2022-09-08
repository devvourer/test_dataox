from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('postgresql://postgres:postgres@db/dataox', echo=True)

Base = declarative_base()


class Apartment(Base):
    __tablename__ = 'Apartments'

    id = Column('id', Integer, primary_key=True)
    image_url = Column('image_url', String(1000), nullable=True)
    title = Column('title', String(255), nullable=True)
    date = Column('date', DateTime)
    seats = Column('seats', String(100), nullable=True)
    description = Column('description', String(1000), nullable=True)
    amount = Column('amount', String(100), nullable=True)
    currency = Column('currency', String(100))
    city = Column('city', String(100))


Base.metadata.create_all(engine)
