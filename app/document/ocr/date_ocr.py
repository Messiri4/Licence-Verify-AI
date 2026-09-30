import cv2
import pytesseract
import re
from collections import Counter


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def normalize_date(text):
    """
    Keep digits only.
    """
    return re.sub(r"[^0-9]", "", text)


def find_dates(text):
    """
    Find YYYY/MM/DD-style dates from OCR output.
    """

    matches = re.findall(
        r"\b(20\d{2})[\s/.-]*(\d{2})[\s/.-]*(\d{2})\b",
        text
    )

    return [
        f"{year}{month}{day}"
        for year, month, day in matches
    ]


def read_single_date(image):
    """
    OCR one isolated date region using multiple
    preprocessing variants.
    """

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

    # Mild blur can reduce card-pattern noise
    blurred = cv2.GaussianBlur(
        gray,
        (3, 3),
        0
    )

    # CLAHE
    clahe = cv2.createCLAHE(
        clipLimit=2.0,
        tileGridSize=(8, 8)
    )

    contrast = clahe.apply(gray)

    # Otsu from original gray
    _, otsu = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    # Otsu after blur
    _, blur_otsu = cv2.threshold(
        blurred,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    variants = {
        "gray": gray,
        "blurred": blurred,
        "contrast": contrast,
        "otsu": otsu,
        "blur_otsu": blur_otsu,
    }

    results = []

    config = (
        "--psm 7 "
        "-c tessedit_char_whitelist=0123456789/"
    )

    for name, variant in variants.items():

        raw = pytesseract.image_to_string(
            variant,
            config=config
        ).strip()

        dates = find_dates(raw)

        results.append({
            "variant": name,
            "raw": raw,
            "dates": dates,
        })

    return results


def read_dates(image_path):
    """
    Read issue and expiry dates independently.
    """

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(
            f"Could not load image: {image_path}"
        )

    date_line = isolate_date_line(image)

    issue_region, expiry_region = (
        split_date_regions(date_line)
    )

    issue_results = read_single_date(
        issue_region
    )

    expiry_results = read_single_date(
        expiry_region
    )

    return {
        "issue": select_date(issue_results),
        "expiry": select_date(expiry_results),
        "attempts": {
            "issue": issue_results,
            "expiry": expiry_results,
        },
    }

def isolate_date_line(image):
    """
    Extract the issue/expiry date row from an already
    extracted licence-number ROI.

    IMPORTANT:
    These coordinates are relative to the licence-number
    ROI, not the full normalized Ontario licence.
    """

    height, width = image.shape[:2]

    y1 = int(height * 0.55)
    y2 = int(height * 1.00)

    return image[
        y1:y2,
        0:width
    ]

def split_date_regions(date_line):
    """
    Split the date row into separate issue-date
    and expiry-date regions, excluding label text.
    """
    height, width = date_line.shape[:2]

    issue_region = date_line[
        0:height,
        int(width * 0.16):int(width * 0.48)
    ]

    expiry_region = date_line[
        0:height,
        int(width * 0.68):width
    ]

    return issue_region, expiry_region

def select_date(results):
    """
    Select a date only when valid OCR candidates agree.
    """

    candidates = []

    for result in results:
        for date in result["dates"]:
            candidates.append(date)

    if not candidates:
        return {
            "date": None,
            "confidence": "none",
            "agreement": 0,
        }

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
    }