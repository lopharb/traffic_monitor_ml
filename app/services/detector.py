import matplotlib.pyplot as plt
import cv2

import numpy as np
from ultralytics import YOLO


class Detector:
    def __init__(self, model_path: str) -> None:
        """
        Initializes the Detector class with a YOLO model and class labels.

        Args:
            model_path (str): The file path to the YOLO model weights.
        """

        self.model = YOLO(model_path)
        self.classes = {1: 'Bus', 2: 'Car', 3: 'Motorcycle', 4: 'Pickup', 5: 'Truck'}

    def _filter_predictions(self, yolo_predictions) -> dict:
        """
        Filters YOLO predictions and organizes them into a dictionary by class name.

        Args:
            yolo_predictions: YOLO prediction results containing bounding boxes and class information.

        Returns:
            A dictionary containing class names as keys and lists of predictions as values. 
            Each prediction is a dictionary with 'confidence' and 'xyxy' keys representing 
            the prediction confidence and bounding box coordinates, respectively.
        """

        results = {}
        for prediction in yolo_predictions[0].boxes:
            class_name = self.classes[prediction.cls.detach().cpu().item()]
            if class_name not in results:
                results[class_name] = []
            results[class_name].append({
                'confidence': prediction.conf.detach().cpu().item(),
                'xyxy': prediction.xyxy[0].detach().cpu().tolist()
            })

        return results

    def get_vehicles(self, image: np.ndarray) -> dict:
        """
        Uses the YOLO model to detect vehicles in an image and 
        organizes the predictions into a dictionary by class name.

        Args:
            image (np.ndarray): The input image to detect vehicles in.

        Returns:
            A dictionary with two keys, 'predictions' and 'frame'. The 'predictions' key points to a dictionary containing class names as keys and lists of predictions as values. Each prediction is a dictionary with 'confidence' and 'xyxy' keys representing the prediction confidence and bounding box coordinates, respectively. The 'frame' key points to the frame image with bounding boxes and class labels superimposed.
        """

        yolo_predictions = self.model.predict(image)
        results = self._filter_predictions(yolo_predictions)
        frame = yolo_predictions[0].plot()

        return {'preditcions': results, 'frame': frame}
