import pandas as pd
from sqlalchemy import Column, MetaData, Table, create_engine, ForeignKey
from sqlalchemy.sql import text
from sqlalchemy.types import Boolean, DateTime, Float, Integer, Text


class Database:
    '''Database client for pandas'''

    def __init__(self, db_uri):
        self.engine = create_engine(
            db_uri, executemany_mode='values',executemany_values_page_size=10000, executemany_batch_page_size=500,
            echo=False) 
            # use executmany_mode with params to speed up insertion

    def create(self):
        '''Create places table if not present already'''
        metadata = MetaData()

        places = Table('places', metadata,
            Column('id', Integer, primary_key=True),
            Column('owner', Text, nullable=True),
            Column('brand', Text, nullable=True),
            Column('type', Text),
            Column('name', Text, nullable=True),
            Column('address', Text),
            Column('town', Text, nullable=True),
            Column('state', Text, nullable=True),
            Column('lat', Float),
            Column('long', Float)
        ) 

        prices = Table('prices', metadata,
            Column('index', Integer, primary_key=True),
            Column('id', Integer, ForeignKey('places.id')),
            Column('gastype', Text),
            Column('price', Float),
            Column('self', Boolean),
            Column('date', DateTime)
            )

        metadata.create_all(self.engine)

    def update_place(self, csv_df, table_name):
        '''Update place table by creating a temp table and then copying it to the final one'''
        # TODO: Maybe clean the temp table? Could it improve performance somehow?
        csv_df.to_sql(
            table_name,
            self.engine,
            if_exists='replace',
            index=True,
            dtype={
                'id': Integer,
                'owner': Text,
                'brand': Text,
                'type': Text,
                'name': Text,
                'address': Text,
                'town': Text,
                'state': Text,
                'lat': Float,
                'long': Float 
            }
        )
        
        sql = text("""INSERT INTO places SELECT * FROM update_places ON CONFLICT DO NOTHING;""") # TODO: not really nice, see if there's a better way without needing two tables

        with self.engine.connect() as con:
            con.execute(sql)

    def update_price(self, csv_df, table_name):
        '''Update price table by creating a temp table and then copying it to the final one'''
        # TODO: Maybe clean the temp table? Could it improve performance somehow?
        csv_df.to_sql(
            table_name,
            self.engine,
            if_exists='replace',
            index=True,
            dtype={
                'index': Integer,
                'id': Integer,
                'gastype': Text,
                'price': Float,
                'self': Boolean,
                'date': DateTime
            }
        )
        
        # TODO: might be useful to pass this query to resolve possible ForeignKey Issues: 
        # UPDATE users SET city_id = NULL WHERE NOT EXISTS(SELECT * FROM cities WHERE city_id = cities.id);

        sql = text("""INSERT INTO prices SELECT * FROM update_prices ON CONFLICT DO NOTHING;""")

        with self.engine.connect() as con:
            con.execute(sql)
