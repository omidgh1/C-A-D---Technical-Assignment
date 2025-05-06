from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import verify_api_key
from app import crud, schemas


router = APIRouter()


@router.post("/measurements/", response_model=schemas.MeasurementOut, dependencies=[Depends(verify_api_key)])
def create(measurement: schemas.MeasurementCreate, db: Session = Depends(get_db)):
    return crud.create_measurement(db, measurement)


@router.get("/measurements/", response_model=list[schemas.MeasurementOut], dependencies=[Depends(verify_api_key)])
def read_all(skip: int = 0, limit: int = 100, source: str = Query(None), db: Session = Depends(get_db)):
    return crud.get_measurements(db, skip, limit, source)


@router.get("/measurements/{measurement_id}", response_model=schemas.MeasurementOut,
            dependencies=[Depends(verify_api_key)])
def read_one(measurement_id: int, db: Session = Depends(get_db)):
    result = crud.get_measurement(db, measurement_id)
    if not result:
        raise HTTPException(status_code=404, detail="ID is Not found")
    return result


@router.put("/measurements/{measurement_id}", response_model=schemas.MeasurementOut,
            dependencies=[Depends(verify_api_key)])
def update(measurement_id: int, measurement: schemas.MeasurementUpdate, db: Session = Depends(get_db)):
    result = crud.update_measurement(db, measurement_id, measurement)
    if not result:
        raise HTTPException(status_code=404, detail="ID is Not found")
    return result


@router.delete("/measurements/{measurement_id}", status_code=204, dependencies=[Depends(verify_api_key)])
def delete(measurement_id: int, db: Session = Depends(get_db)):
    result = crud.delete_measurement(db, measurement_id)
    if not result:
        raise HTTPException(status_code=404, detail="ID is Not found")
    return
