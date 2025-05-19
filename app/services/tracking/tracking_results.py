from datetime import datetime

from ..database.connector import SessionLocal
from ..database.models import CameraStats


class TrackedCameraStats:
    def __init__(self):
        # { camera_id: { date: { class_name: { track_id: count } } }
        self.seen_ids = {}

    def process_detections(self, camera_id, detections):

        today = datetime.now().date().strftime("%Y-%m-%d")

        if camera_id not in self.seen_ids:
            self.seen_ids[camera_id] = {}

        cam_data = self.seen_ids[camera_id]

        if today not in cam_data:
            cam_data[today] = {
                "Bus": set(),
                "Car": set(),
                "Motorcycle": set(),
                "Pickup": set(),
                "Truck": set()
            }

        daily_tracker = cam_data[today]

        for cls_name, preds in detections.items():
            for pred in preds:
                track_id = pred['track_id']
                if cls_name in daily_tracker and track_id not in daily_tracker[cls_name]:
                    # Increment DB
                    self._update_database(camera_id, today, cls_name)
                    daily_tracker[cls_name].add(track_id)

    def _update_database(self, camera_id, date, class_name):
        """Updates the camera stats table with one new detection"""
        stat_table_map = {
            "Bus": "bus_count",
            "Car": "car_count",
            "Motorcycle": "motorcycle_count",
            "Pickup": "pickup_count",
            "Truck": "truck_count"
        }

        column = stat_table_map.get(class_name, None)
        if not column:
            return

        session = SessionLocal()
        try:
            stat = (
                session.query(CameraStats)
                .filter(
                    CameraStats.camera_id == camera_id,
                    CameraStats.date == date
                )
                .first()
            )

            if stat:
                current = getattr(stat, column)
                setattr(stat, column, current + 1)
            else:
                new_stat = CameraStats(
                    camera_id=camera_id,
                    date=date,
                    **{column: 1}
                )
                session.add(new_stat)

            session.commit()
        except Exception as e:
            session.rollback()
            print("Error updating stats:", str(e))
        finally:
            if session:
                session.close()
