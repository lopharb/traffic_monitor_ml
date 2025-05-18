# models.py

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class CameraMarker(Base):
    __tablename__ = 'camera_markers'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)

    # Relationship to stats
    stats = relationship("CameraStats", back_populates="camera")

    def __repr__(self):
        return f"<CameraMarker(id={self.id}, name='{self.name}', lat={self.latitude}, lng={self.longitude})>"


class CameraStats(Base):
    __tablename__ = 'camera_stats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    camera_id = Column(Integer, ForeignKey('camera_markers.id'), nullable=False)
    date = Column(Date, nullable=False)

    bus_count = Column(Integer, default=0)
    car_count = Column(Integer, default=0)
    motorcycle_count = Column(Integer, default=0)
    pickup_count = Column(Integer, default=0)
    truck_count = Column(Integer, default=0)
    unknown_count = Column(Integer, default=0)

    # Relationship back to camera
    camera = relationship("CameraMarker", back_populates="stats")

    def __repr__(self):
        return f"<CameraStats(camera_id={self.camera_id}, date='{self.date}')>"
