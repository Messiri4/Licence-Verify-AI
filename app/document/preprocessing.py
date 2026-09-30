import cv2
import numpy as np


def enhance_licence(image):
    gray = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2GRAY
    )

    clahe = cv2.createCLAHE(
        clipLimit=3.0,
        tileGridSize=(8, 8)
    )

    enhanced = clahe.apply(gray)

    denoised = cv2.bilateralFilter(
        enhanced,
        7,
        50,
        50
    )

    blurred = cv2.GaussianBlur(
        denoised,
        (0, 0),
        2
    )

    return cv2.addWeighted(
        denoised,
        1.7,
        blurred,
        -0.7,
        0
    )


def gamma_correction(
    image,
    gamma=1.8
):
    normalized = image / 255.0

    corrected = np.power(
        normalized,
        1 / gamma
    )

    return (
        corrected * 255
    ).astype("uint8")