import cv2
import pytesseract
import re
from collections import Counter


pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

WHITELIST = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-"


def isolate_licence_number_line(image):
    """
    Extract the licence-number row from the ROI.
    """
    height, width = image.shape[:2]

    y1 = int(height * 0.20)
    y2 = int(height * 0.72)
    x1 = int(width * 0.14)

    return image[
        y1:y2,
        x1:width
    ]


def preprocess_variants(image):
    image = isolate_licence_number_line(image)

    enlarged = cv2.resize(
        image,
        None,
        fx=4,
        fy=4,
        interpolation=cv2.INTER_CUBIC
    )

    gray = cv2.cvtColor(
        enlarged,
        cv2.COLOR_BGR2GRAY
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

    _, otsu_inv = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    return {
        "gray": gray,
        "contrast": contrast,
        "otsu": otsu,
        "otsu_inv": otsu_inv,
    }


def normalize_number(text):
    return re.sub(
        r"[^A-Z0-9]",
        "",
        text.upper()
    )


def is_valid_ontario_number(value):
    """
    Ontario licence number:
    1 letter + 14 digits.
    """
    return bool(
        re.fullmatch(
            r"[A-Z][0-9]{14}",
            value
        )
    )


def format_licence_number(value):
    """
    E54141670816027
        ↓
    E5414-16708-16027
    """
    if not is_valid_ontario_number(value):
        return value

    return (
        f"{value[:5]}-"
        f"{value[5:10]}-"
        f"{value[10:]}"
    )


def run_tesseract(image, psm):
    config = (
        f"--psm {psm} "
        f"-c tessedit_char_whitelist={WHITELIST}"
    )

    return pytesseract.image_to_string(
        image,
        config=config
    ).strip()


def read_licence_number(image_path):
    """
    Run multiple OCR attempts and select the valid
    licence number with the strongest agreement.
    """

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(
            f"Could not load image: {image_path}"
        )

    variants = preprocess_variants(image)

    valid_candidates = []

    attempts = []

    for variant_name, variant in variants.items():

        for psm in [6, 7, 8, 13]:

            raw = run_tesseract(
                variant,
                psm
            )

            normalized = normalize_number(raw)

            valid = is_valid_ontario_number(
                normalized
            )

            attempts.append({
                "variant": variant_name,
                "psm": psm,
                "raw": raw,
                "normalized": normalized,
                "valid": valid,
            })

            if valid:
                valid_candidates.append(
                    normalized
                )

    if not valid_candidates:
        return {
            "licence_number": None,
            "formatted": None,
            "confidence": "none",
            "agreement": 0,
            "attempts": attempts,
        }

    counts = Counter(valid_candidates)

    best_number, agreement = (
        counts.most_common(1)[0]
    )

    total_valid = len(valid_candidates)

    agreement_ratio = (
        agreement / total_valid
    )

    if agreement >= 3 and agreement_ratio >= 0.60:
        confidence = "high"
    elif agreement >= 2:
        confidence = "medium"
    else:
        confidence = "low"

    return {
        "licence_number": best_number,
        "formatted": format_licence_number(
            best_number
        ),
        "confidence": confidence,
        "agreement": agreement,
        "valid_attempts": total_valid,
        "attempts": attempts,
    }