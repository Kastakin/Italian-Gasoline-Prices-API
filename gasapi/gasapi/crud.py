from sqlalchemy.orm import Session
from sqlalchemy import and_
from math import cos, radians, degrees, asin
from . import models, schemas

def get_place(db: Session, place_id: int):
    return db.query(models.Place).filter(models.Place.id == place_id).first()

def get_places(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Place).filter(models.Place.prices.any()).order_by(models.Place.id.asc()).offset(skip).limit(limit).all()

def get_in_radius(db: Session, lat: float, long: float, radius: int = 15):
    R = 6371 # radius of heart in km
    maxlat = lat + degrees(radius/R)
    minlat = lat - degrees(radius/R)
    maxlong = long + degrees(asin(radius/R) / cos(radians(lat)))
    minlong = long - degrees(asin(radius/R) / cos(radians(lat)))

    return db.query(models.Place).filter(and_(models.Place.lat.between(minlat, maxlat), models.Place.long.between(minlong, maxlong))).all()


    