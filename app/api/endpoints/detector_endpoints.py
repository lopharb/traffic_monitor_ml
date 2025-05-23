import cv2
import numpy as np
from fastapi import APIRouter, File, UploadFile
from fastapi.responses import StreamingResponse

from ...services.detector import Detector
from ...services.tracking.tracking_results import TrackedCameraStats
from ..schemas.detections import PredictionResponse

detector_router = APIRouter(prefix='/api/v1/detect')


detector = Detector(model_path="notebooks/runs/train/traffic_yolo/weights/best.pt")


@detector_router.post("/predict_frame", response_model=PredictionResponse)
async def predict_frame(file: UploadFile = File(...)):
    contents = await file.read()
    nparr = np.frombuffer(contents, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    result = detector.get_vehicles(frame)
    return {"predictions": result["preditcions"]}


@detector_router.get("/video_stream/{cam_id}")
async def video_stream(cam_id: int):
    # TODO redo this with streaming video
    # with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_file:
    #     shutil.copyfileobj(file.file, temp_file)
    #     temp_filename = temp_file.name
    tracked_stats = TrackedCameraStats()

    def generate(cam_id):
        cap = cv2.VideoCapture('video.mp4')
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            result = detector.get_vehicles(frame)
            frame = result['frame']

            tracked_stats.process_detections(cam_id, result['predictions'])

            _, buffer = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        cap.release()

    return StreamingResponse(generate(cam_id), media_type='multipart/x-mixed-replace; boundary=frame')
