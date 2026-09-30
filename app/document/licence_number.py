import cv2
import re

from app.document.templates import get_template
from app.document.roi import extract_template_field


def extract_number_roi(
    licence_image,
    template_name="ontario_new"
):
    template = get_template(
        template_name
    )

    field = template[
        "licence_number"
    ]

    return extract_template_field(
        licence_image,
        field
    )


def make_ocr_variants(roi):
    enlarged = cv2.resize(
        roi,
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
        clipLimit=1.5,
        tileGridSize=(8, 8)
    )

    contrast = clahe.apply(gray)

    _, otsu = cv2.threshold(
        gray,
        0,
        255,
        cv2.THRESH_BINARY
        + cv2.THRESH_OTSU
    )

    adaptive = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        7
    )

    return {
        "gray": gray,
        "contrast": contrast,
        "otsu": otsu,
        "adaptive": adaptive,
    }


def normalize_licence_number(text):
    return re.sub(
        r"[^A-Z0-9]",
        "",
        text.upper()
    )


def is_valid_ontario_format(text):
    cleaned = (
        normalize_licence_number(
            text
        )
    )

    return bool(
        re.fullmatch(
            r"[A-Z]\d{14}",
            cleaned
        )
    )