import tempfile
import shutil
from fastapi import UploadFile, File
from fastapi.responses import StreamingResponse
import numpy as np
import cv2
from app.api.schemas.detections import PredictionResponse
from fastapi import APIRouter
from app.services.detector import Detector


detector_router = APIRouter(prefix='/api/v1/detect')


detector = Detector(model_path="notebooks/runs/train/traffic_yolo/weights/best.pt")


@detector_router.post("/predict_frame", response_model=PredictionResponse)
async def predict_frame(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    result = detector.get_vehicles(frame)
    return {"predictions": result["preditcions"]}


@detector_router.get("/video_stream")
async def video_stream():
    # TODO redo this with streaming video
    # with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
    #     shutil.copyfileobj(file.file, temp_file)
    #     temp_filename = temp_file.name

    def generate():
        cap = cv2.VideoCapture('video.mp4')
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            result = detector.get_vehicles(frame)
            frame = result['frame']

            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        cap.release()

    return StreamingResponse(generate(), media_type='multipart/x-mixed-replace; boundary=frame')
