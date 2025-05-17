from fastapi import APIRouter


marker_router = APIRouter(prefix='/api/v1/markers')


@marker_router.get("/ping")
async def ping():
    return {"message": "pong"}


@marker_router.get("/")
async def get_markers():
    markers = [
        {"id": 1, "position": [53.893009,  27.567444], "name": "Marker 1",
            "streamUrl": "detect/video_stream"},
        {"id": 2, "position": [53.90, 27.577444], "name": "Marker 2",
            "streamUrl": "detect/video_stream"},
    ]
    return markers
