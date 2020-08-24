from typing import List
from fastapi import Depends, FastAPI, HTTPException, Request
from sqlalchemy.orm import Session

from . import app, crud, models, query_tags, schemas, templates
from .database import SessionLocal, engine

# Dependency


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

### Places Query ###

@app.get("/places/", response_model=List[schemas.SimplePlace], tags=['Places'])
def get_places(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    '''Returns a list of places'''
    db_places = crud.get_places(db, skip=skip, limit=limit)
    return db_places

@app.get("/places_in_radius/", response_model=List[schemas.Place], tags=['Places'])
def get_in_radius(lat: float, long: float, radius: int = 15, db: Session = Depends(get_db)):
    '''Returns a list of places inside defined radius (in km) centered on the defined point (latitude and longitude)'''
    db_in_radius = crud.get_in_radius(db, lat=lat, long=long, radius=radius)
    if db_in_radius == []:
        raise HTTPException(status_code=404, detail="No places in radius")
    return db_in_radius

### Prices Query ###

@app.get("/prices/{place_id}", response_model=schemas.Place, tags=['Prices'])
def get_place(place_id: int, db: Session = Depends(get_db)):
    '''Returns the prices for the gas station with the requested ID, if not found returns 404'''
    db_place = crud.get_place(db, place_id=place_id)
    if db_place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    if db_place.prices == []:
        raise HTTPException(status_code=403, detail="No recent prices")
    return db_place