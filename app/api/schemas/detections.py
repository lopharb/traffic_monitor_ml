from pydantic import BaseModel
from typing import List, Dict


class Prediction(BaseModel):
    class_name: str
    confidence: float
    xyxy: List[float]  # [x1, y1, x2, y2]


class PredictionResponse(BaseModel):
    predictions: Dict[str, List[Prediction]]
