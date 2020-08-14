# coding: utf-8
from sqlalchemy import (Boolean, Column, DateTime, Float, ForeignKey, Integer,
                        Table, Text, text)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from gasapi.database import Base


class Place(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True, server_default=text(
        "nextval('places_id_seq'::regclass)"))
    owner = Column(Text)
    brand = Column(Text)
    type = Column(Text)
    name = Column(Text)
    address = Column(Text)
    town = Column(Text)
    state = Column(Text)
    lat = Column(Float(53))
    long = Column(Float(53))

    prices = relationship('Price', back_populates='place')


class Price(Base):
    __tablename__ = 'prices'

    index = Column(Integer, primary_key=True)
    id = Column(Integer, ForeignKey('places.id'))
    gastype = Column(Text)
    price = Column(Float(53))
    self = Column(Boolean)
    date = Column(DateTime)

    place = relationship('Place', back_populates='prices')
