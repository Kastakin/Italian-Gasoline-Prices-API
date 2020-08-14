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


@app.get("/places/{place_id}", response_model=schemas.Place, tags=['Places'])
def get_place(place_id: int, db: Session = Depends(get_db)):
    '''Returns the place with the requested ID and its prices, if not found returns 404'''
    db_place = crud.get_place(db, place_id=place_id)
    if db_place is None:
        raise HTTPException(status_code=404, detail="Place not found")
    if db_place.prices == []:
        raise HTTPException(status_code=403, detail="No recent prices")
    return db_place


@app.get("/places/", response_model=List[schemas.Place], tags=['Places'])
def get_places(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    '''Returns a list of places'''
    db_places = crud.get_places(db, skip=skip, limit=limit)
    return db_places

# TODO: implement a way to find closest place
# @app.get("/closest/", response_model=schemas.Place, tags=['Places'])
# def get_closest(lat: float, long: float, db: Session=Depends(get_db)):
#     db_closest = crud.get_closest(db, lat=lat, long=long)
#     return db_closest
