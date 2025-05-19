from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException

from ...services.database.models import CameraStats

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


@marker_router.get("/stats/{camera_id}")
def get_camera_stats(
    camera_id: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    db_manager = DatabaseManager()
    try:
        parsed_start = None
        parsed_end = None

        if start_date:
            parsed_start = datetime.strptime(start_date, "%Y-%m-%d").date()
        if end_date:
            parsed_end = datetime.strptime(end_date, "%Y-%m-%d").date()

        stats = db_manager.get_camera_stats(camera_id, parsed_start, parsed_end)

        if not stats:
            raise HTTPException(status_code=404, detail="No stats found")

        return {
            "camera_id": camera_id,
            "time_range": {
                "start_date": start_date or "unspecified",
                "end_date": end_date or "unspecified"
            },
            "stats": stats
        }

    except ValueError as ve:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")
