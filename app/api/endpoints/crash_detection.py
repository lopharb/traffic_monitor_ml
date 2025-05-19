import cv2
from fastapi import APIRouter, File, UploadFile
import numpy as np

crash_router = APIRouter(prefix='/api/v1/crash')


@crash_router.get("/ping")
async def ping():
    return {"message": "pong"}


@crash_router.get("/predict_frame/{cam_id}")
async def predict_frame(cam_id: int):
    # contents = await file.read()
    # nparr = np.frombuffer(contents, np.uint8)
    # _frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    random_int = np.random.randint(0, 5)
    random_bool = True if random_int == 1 else False
    random_float = np.random.uniform(0, 1)

    return {
        'is_crash': random_bool,
        'confidence': random_float
    }
