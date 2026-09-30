import base64
import os
import cv2

import requests
from dotenv import load_dotenv

load_dotenv()

ROBOFLOW_MODEL_URL = (
    "https://serverless.roboflow.com/"
    "ocr-rxfo5/driver_license_detector_old_new-instant-1"
)


def detect_licence(image_path):
    api_key = os.getenv("ROBOFLOW_API_KEY")

    if not api_key:
        raise RuntimeError(
            "ROBOFLOW_API_KEY is not configured."
        )

    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(
            image_file.read()
        ).decode("utf-8")

    response = requests.post(
        f"{ROBOFLOW_MODEL_URL}?api_key={api_key}",
        data=image_data,
        headers={
            "Content-Type":
            "application/x-www-form-urlencoded"
        },
        timeout=30
    )

    response.raise_for_status()

    result = response.json()

    predictions = result.get(
        "predictions",
        []
    )

    if not predictions:
        return None

    return max(
        predictions,
        key=lambda prediction:
        prediction["confidence"]
    )



def draw_detection(image_path, detection):
    image = cv2.imread(str(image_path))

    if image is None:
        raise FileNotFoundError(
            f"Could not read image: {image_path}"
        )

    x = detection["x"]
    y = detection["y"]
    width = detection["width"]
    height = detection["height"]
    confidence = detection["confidence"]
    class_name = detection["class"]

    # Roboflow gives center x/y + width/height
    x1 = int(x - width / 2)
    y1 = int(y - height / 2)

    x2 = int(x + width / 2)
    y2 = int(y + height / 2)

    # Draw bounding box
    cv2.rectangle(
        image,
        (x1, y1),
        (x2, y2),
        (0, 255, 0),
        3
    )

    label = (
        f"{class_name}: "
        f"{confidence:.2f}"
    )

    cv2.putText(
        image,
        label,
        (x1, max(y1 - 10, 30)),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 0),
        2
    )

    return image