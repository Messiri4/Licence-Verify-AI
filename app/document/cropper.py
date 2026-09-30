import cv2


def crop_licence(image_path, detection):
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(
            f"Could not read image: {image_path}"
        )

    x = detection["x"]
    y = detection["y"]
    width = detection["width"]
    height = detection["height"]

    x1 = int(x - width / 2)
    y1 = int(y - height / 2)

    x2 = int(x + width / 2)
    y2 = int(y + height / 2)

    image_height, image_width = (
        image.shape[:2]
    )

    x1 = max(0, x1)
    y1 = max(0, y1)

    x2 = min(
        image_width,
        x2
    )

    y2 = min(
        image_height,
        y2
    )

    return image[
        y1:y2,
        x1:x2
    ]