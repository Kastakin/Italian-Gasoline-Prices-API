from typing import List
from datetime import date

from pydantic import BaseModel


class SimplePrice(BaseModel):
    gastype: str
    price: float
    self: bool

    class Config:
        orm_mode = True

class Price(SimplePrice):
    id: int
    date: date

class SimplePlace(BaseModel):
    id: int
    owner: str = None
    brand: str = None
    type: str
    name: str = None
    address: str
    town: str = None
    state: str = None
    lat: float
    long: float

    class Config:
        orm_mode = True

class Place(SimplePlace):
    

    prices: List[SimplePrice] = []

