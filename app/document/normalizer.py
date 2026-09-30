import cv2


STANDARD_WIDTH = 1012
STANDARD_HEIGHT = 638


def normalize_licence(licence_image):
    """
    Resize an already-cropped licence to a standard ID-card size.

    This does not yet perform full perspective correction.
    It gives all downstream field extraction code a consistent size.
    """

    if licence_image is None:
        raise ValueError(
            "licence_image cannot be None"
        )

    normalized = cv2.resize(
        licence_image,
        (STANDARD_WIDTH, STANDARD_HEIGHT),
        interpolation=cv2.INTER_CUBIC
    )

    return normalized