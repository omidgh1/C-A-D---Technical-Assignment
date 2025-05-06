from sqlalchemy.orm import Session
from app.models import Measurement
from app.schemas import MeasurementCreate, MeasurementUpdate


def get_measurements(db: Session, skip: int = 0, limit: int = 100, source: str = None):
    query = db.query(Measurement)
    if source:
        query = query.filter(Measurement.source == source)
    return query.offset(skip).limit(limit).all()


def get_measurement(db: Session, measurement_id: int):
    return db.query(Measurement).filter(Measurement.id == measurement_id).first()


def create_measurement(db: Session, measurement: MeasurementCreate):
    db_item = Measurement(**measurement.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def update_measurement(db: Session, measurement_id: int, measurement: MeasurementUpdate):
    db_item = get_measurement(db, measurement_id)
    if not db_item:
        return None
    for key, value in measurement.model_dump(exclude_unset=True).items():
        setattr(db_item, key, value)
    db.commit()
    return db_item


def delete_measurement(db: Session, measurement_id: int):
    db_item = get_measurement(db, measurement_id)
    if not db_item:
        return None
    db.delete(db_item)
    db.commit()
    return db_item
