from datetime import date, timedelta
from .models import CameraMarker, CameraStats, User
from .connector import SessionLocal
from .. import auth


class DatabaseManager:
    def __init__(self):
        self.SessionLocal = SessionLocal

    def get_session(self):
        return self.SessionLocal()

    def add_camera(self, name: str, latitude: float, longitude: float):
        session = self.get_session()
        try:
            camera = CameraMarker(name=name, latitude=latitude, longitude=longitude)
            session.add(camera)
            session.commit()
            session.refresh(camera)
            return camera
        finally:
            session.close()

    def get_all_cameras(self):
        session = self.get_session()
        try:
            return session.query(CameraMarker).all()
        finally:
            session.close()

    def get_camera_by_id(self, camera_id: int):
        session = self.get_session()
        try:
            return session.query(CameraMarker).filter(CameraMarker.id == camera_id).first()
        finally:
            session.close()

    def update_camera(self, camera_id: int, name: str = None, latitude: float = None, longitude: float = None):
        session = self.get_session()
        try:
            camera = session.query(CameraMarker).filter(CameraMarker.id == camera_id).first()
            if not camera:
                return None

            if name is not None:
                camera.name = name
            if latitude is not None:
                camera.latitude = latitude
            if longitude is not None:
                camera.longitude = longitude

            session.commit()
            session.refresh(camera)
            return camera
        finally:
            session.close()

    def delete_camera(self, camera_id: int):
        session = self.get_session()
        try:
            camera = session.query(CameraMarker).filter(CameraMarker.id == camera_id).first()
            if camera:
                session.delete(camera)
                session.commit()
                return True
            return False
        finally:
            session.close()

    def add_camera_stats(self, camera_id: int, date: str,
                         bus_count: int = 0,
                         car_count: int = 0,
                         motorcycle_count: int = 0,
                         truck_count: int = 0,
                         pickup_count: int = 0,
                         unknown_count: int = 0):
        session = self.get_session()
        try:
            stats = CameraStats(
                camera_id=camera_id,
                date=date,
                bus_count=bus_count,
                car_count=car_count,
                motorcycle_count=motorcycle_count,
                pickup_count=pickup_count,
                truck_count=truck_count,
                unknown_count=unknown_count
            )
            session.add(stats)
            session.commit()
            session.refresh(stats)
            return stats
        finally:
            session.close()

    def get_camera_stats(self, camera_id: int, start_date: date = None, end_date: date = None):
        session = self.get_session()
        try:
            query = session.query(CameraStats).filter(CameraStats.camera_id == camera_id)
            if end_date is None:
                end_date = date.today()

            if start_date is None:
                start_date = end_date - timedelta(days=14)

            # Apply date filter if dates are provided
            if start_date and end_date:
                query = query.filter(
                    CameraStats.date >= start_date,
                    CameraStats.date <= end_date
                )
            elif start_date:
                query = query.filter(CameraStats.date >= start_date)
            elif end_date:
                query = query.filter(CameraStats.date <= end_date)

            return query.all()
        finally:
            session.close()

    def get_stats_by_date(self, camera_id: int, date: str):
        session = self.get_session()
        try:
            return session.query(CameraStats).filter(
                CameraStats.camera_id == camera_id,
                CameraStats.date == date
            ).first()
        finally:
            session.close()

    def get_user_by_username(self, username: str):
        session = self.get_session()
        try:
            return session.query(User).filter(User.username == username).first()
        finally:
            session.close()

    def get_user_by_email(self, email: str):
        session = self.get_session()
        try:
            return session.query(User).filter(User.email == email).first()
        finally:
            session.close()

    def create_user(self, username: str, email: str, password: str):
        session = self.get_session()
        try:
            hashed_pw = auth.get_password_hash(password)
            user = User(username=username, email=email, hashed_password=hashed_pw)
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
        finally:
            session.close()
