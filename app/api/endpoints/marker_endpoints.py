from fastapi import APIRouter
from ...services.database.db import DatabaseManager


marker_router = APIRouter(prefix='/api/v1/markers')


@marker_router.get("/ping")
async def ping():
    return {"message": "pong"}


@marker_router.get("/")
async def get_markers():
    db_manager = DatabaseManager()
    camera_markers = db_manager.get_all_cameras()
    markers = []
    for cam in camera_markers:
        markers.append({
            "id": cam.id,
            "position": [cam.latitude, cam.longitude],
            "name": cam.name,
            "streamUrl": "detect/video_stream"  # or use dynamic stream URLs
        })
    return markers
