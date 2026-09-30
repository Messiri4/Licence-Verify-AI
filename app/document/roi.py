def extract_region(image, region):
    """
    Extract a normalized rectangular region from an image.

    region:
        (x1, y1, x2, y2)

    Coordinates are normalized between 0 and 1.
    """

    if image is None:
        raise ValueError("Image cannot be None.")

    height, width = image.shape[:2]

    x1, y1, x2, y2 = region

    x1 = int(width * x1)
    y1 = int(height * y1)
    x2 = int(width * x2)
    y2 = int(height * y2)

    return image[
        y1:y2,
        x1:x2
    ]


def extract_template_field(image, field_config):
    """
    Extract a field defined by a licence template.

    field_config must contain:
        x1, y1, x2, y2
    """

    region = (
        field_config["x1"],
        field_config["y1"],
        field_config["x2"],
        field_config["y2"],
    )

    return extract_region(
        image,
        region
    )