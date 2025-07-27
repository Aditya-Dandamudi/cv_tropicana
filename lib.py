from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import tempfile
import os


def load_model(weights_path):
    return YOLO(weights_path)

def predict_image(model, image, conf_threshold=0.25):
    results = model.predict(image, conf=conf_threshold, verbose=False)
    boxes = results[0].boxes

    if boxes is None or len(boxes) == 0:
        return image, None  # No detections

    # Get top scoring box
    scores = boxes.conf.cpu().numpy()
    class_ids = boxes.cls.cpu().numpy()
    names = results[0].names

    top_idx = scores.argmax()
    top_score = scores[top_idx]
    top_class = int(class_ids[top_idx])
    top_label = names[top_class]

    label_str = f"We are {top_score*100:.1f}% sure that the product is {top_label}."

    return image, label_str
