from sqlalchemy.orm import Session
from math import cos
from . import models, schemas

def get_place(db: Session, place_id: int):
    return db.query(models.Place).filter(models.Place.id == place_id).first()

def get_places(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Place).filter(models.Place.prices.any()).order_by(models.Place.id.asc()).offset(skip).limit(limit).all()



    