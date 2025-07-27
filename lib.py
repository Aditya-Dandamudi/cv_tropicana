
# from ultralytics import YOLO
# import numpy as np
# from PIL import Image


# def load_model(model_path: str):
#     return YOLO(model_path)


# def predict_top_label(model, image: Image.Image, conf_threshold: float = 0.25):
#     """Run prediction and return only the most confident result."""
#     img_np = np.array(image.convert("RGB"))
#     results = model.predict(img_np, conf=conf_threshold)[0]
#     boxes = results.boxes
#     class_names = model.names

#     if boxes and boxes.conf is not None and len(boxes.conf) > 0:
#         # Get index of highest confidence score
#         top_idx = boxes.conf.argmax()
#         top_cls = int(boxes.cls[top_idx])
#         top_conf = float(boxes.conf[top_idx])
#         label = class_names[top_cls]
#         return f"We are {top_conf * 100:.1f}% sure that the product is {label}."

#     return None  # No predictions above threshold




from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import tempfile
import os


def load_model(model_path: str):
    return YOLO(model_path)


def predict_image(model, image: Image.Image, conf_threshold=0.1):
    """
    Run YOLOv8 prediction on a PIL image using image path inference
    for consistent preprocessing with Colab behavior.
    """
    img_rgb = image.convert("RGB")

    # Save image temporarily to disk and get path
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        tmp_path = tmp.name
        img_rgb.save(tmp_path)

    # Use image path for prediction (matches Colab behavior)
    results = model(tmp_path, conf=conf_threshold, imgsz=640, verbose=False)[0]

    # Cleanup temp file after use
    os.remove(tmp_path)

    return draw_top_box(np.array(img_rgb), results, model.names)


def draw_top_box(image, results, class_names):
    """Draw only the highest-confidence bounding box on the image."""
    boxes = results.boxes

    if boxes and boxes.xyxy is not None and len(boxes) > 0:
        # Find box with highest confidence
        best_idx = boxes.conf.argmax().item()

        x1, y1, x2, y2 = map(int, boxes.xyxy[best_idx])
        cls = int(boxes.cls[best_idx])
        conf = float(boxes.conf[best_idx])
        label = f"{class_names[cls]} {conf:.2f}"

        # Draw bounding box
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 128, 255), 3, lineType=cv2.LINE_AA)

        # Draw label background
        (tw, th), baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
        margin = 5
        if y1 - th - 2 * margin > 0:
            text_org = (x1 + margin, y1 - margin)
            rect_top = y1 - th - 2 * margin
            rect_bottom = y1
        else:
            text_org = (x1 + margin, y1 + th + margin)
            rect_top = y1
            rect_bottom = y1 + th + 2 * margin

        cv2.rectangle(image, (x1, rect_top), (x1 + tw + 2 * margin, rect_bottom), (0, 128, 255), -1)
        cv2.putText(image, label, text_org, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2, lineType=cv2.LINE_AA)

    return image
