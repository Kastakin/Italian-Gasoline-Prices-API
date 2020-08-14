from config import CSV_PLACE, CSV_PRICE, DB_URI
import functools
from .database import Database
from .dataframe import load_place, load_price

# This decorator can be applied to
def with_logging(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print('LOG: Running job "%s"' % func.__name__)
        result = func(*args, **kwargs)
        print('LOG: Job "%s" completed' % func.__name__)
        return result
    return wrapper

@with_logging
def table_creator():
    '''Creates required tables if not already present'''
    db = Database(DB_URI)
    create = db.create()
    return create

@with_logging
def db_updater():
    '''Load csv data from source and updates the DB'''
    df_place = load_place(CSV_PLACE)
    df_price = load_price(CSV_PRICE)
    db = Database(DB_URI)
    update_place = db.update_place(df_place, 'update_places')
    update_price = db.update_price(df_price, 'update_prices')
    return update_place, update_price
