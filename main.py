from app.api.endpoints import detector_router
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Transport Monitoring Tool API",
    description="API for Transport Monitoring Tool",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detector_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=False)
