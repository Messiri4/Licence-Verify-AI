import cv2
import pytesseract
import re
from collections import Counter


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def isolate_dob_date(image):
    """
    Extract only the printed DOB value from dob_roi.jpg.

    dob_roi.jpg already contains the bottom-left DOB area,
    so this removes the DOB/DN label and surrounding noise.
    """
    height, width = image.shape[:2]

    dob_date = image[
        int(height * 0.35):int(height * 0.95),
        int(width * 0.30):int(width * 0.95)
    ]

    return dob_date


def find_dob(text):
    """
    Find YYYY/MM/DD-style dates.
    """
    matches = re.findall(
        r"\b(19\d{2}|20\d{2})[\s/.-]*(\d{2})[\s/.-]*(\d{2})\b",
        text
    )

    return [
        f"{year}{month}{day}"
        for year, month, day in matches
    ]


def read_dob(image_path):
    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(
            f"Could not load image: {image_path}"
        )

    # IMPORTANT:
    # dob_roi.jpg is already cropped correctly,
    # so do NOT crop it again for this test.

    # Isolate only the DOB value
    image = isolate_dob_date(image)

    # Add white padding around the ROI
    image = cv2.copyMakeBorder(
        image,
        20,
        20,
        20,
        20,
        cv2.BORDER_CONSTANT,
        value=(255, 255, 255)
    )

    # Save debug image
    cv2.imwrite(
        "data/output/dob_date_line.jpg",
        image
    )

    # Enlarge image
    enlarged = cv2.resize(
        image,
        None,
        fx=6,
        fy=6,
        interpolation=cv2.INTER_CUBIC
    )

    gray = cv2.cvtColor(
        enlarged,
        cv2.COLOR_BGR2GRAY
    )

    blurred = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    contrast = clahe.apply(gray)

    _, otsu = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    variants = {
        "gray": gray,
        "blurred": blurred,
        "contrast": contrast,
        "otsu": otsu,
    }

    results = []
    candidates = []

    for name, variant in variants.items():

        for psm in [6, 7, 8, 13]:

            config = (
                f"--psm {psm} "
                "-c tessedit_char_whitelist=0123456789/"
            )

            raw = pytesseract.image_to_string(
                variant,
                config=config
            ).strip()

            dates = find_dob(raw)

            results.append({
                "variant": name,
                "psm": psm,
                "raw": raw,
                "dates": dates,
            })

            candidates.extend(dates)

    # No valid DOB found
    if not candidates:
        return {
            "date": None,
            "confidence": "none",
            "agreement": 0,
            "attempts": results,
        }

    # Vote among valid DOB candidates
    counts = Counter(candidates)

    best_date, agreement = counts.most_common(1)[0]

    if agreement >= 3:
        confidence = "high"

    elif agreement >= 2:
        confidence = "medium"

    else:
        confidence = "low"

    return {
        "date": best_date,
        "confidence": confidence,
        "agreement": agreement,
        "attempts": results,
    }