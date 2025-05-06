from pydantic import BaseModel, ConfigDict
from typing import Optional


class MeasurementBase(BaseModel):
    co2_value: float
    unit: Optional[str] = "ppm"
    source: Optional[str] = "unknown"
    description: Optional[str] = None


class MeasurementCreate(MeasurementBase):
    pass


class MeasurementUpdate(MeasurementBase):
    pass


class MeasurementOut(MeasurementBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
