import cv2
import zxingcpp
from pathlib import Path


def extract_barcode_region(image_path, output_path=None):
    """
    Extract the approximate PDF417 region from the
    normalized/back licence image.

    Current coordinates are broad so that we don't
    accidentally clip the barcode.
    """

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(
            f"Could not load image: {image_path}"
        )

    height, width = image.shape[:2]

    # Barcode is in the lower portion of an Ontario licence back.
    x1 = int(width * 0.10)
    x2 = int(width * 0.90)

    y1 = int(height * 0.50)
    y2 = int(height * 0.90)

    crop = image[y1:y2, x1:x2]

    # Upscale for barcode decoding
    crop = cv2.resize(
        crop,
        None,
        fx=3,
        fy=3,
        interpolation=cv2.INTER_CUBIC
    )

    if output_path:
        Path(output_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        cv2.imwrite(
            output_path,
            crop
        )

    return crop


def decode_barcode(image_path):

    barcode_image = extract_barcode_region(
        image_path,
        output_path="data/output/barcode_roi.jpg"
    )

    results = zxingcpp.read_barcodes(
        barcode_image
    )

    decoded = []

    for result in results:

        decoded.append({
            "format": str(result.format),
            "text": result.text,
        })

    return decoded