from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from decouple import config
from datetime import datetime, timedelta

from .models import Apartment

engine = create_engine(config('db_config'))

session = sessionmaker(bind=engine)
s = session()

rows = s.query(Apartment).filter(Apartment.id > 1)

for row in rows:
    print(row)


def set_values(data):
    s.bulk_save_objects(data)
    s.commit()


def format_date(date: str) -> datetime:
    if date.startswith('<'):
        hours = date.split(' ')[1]

        time = datetime.now()
        return time - timedelta(hours=int(hours))
    split_date = date.split('/')
    month = split_date[1].replace('0', '', 1) if split_date.startswith('0') else split_date[1]
    day = split_date[0].replace('0', '', 1) if split_date.startswith('0') else split_date[0]

    time = datetime(year=split_date[-2], month=month, day=day)

    return time

