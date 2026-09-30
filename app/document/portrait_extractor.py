import cv2
from pathlib import Path

from app.document.templates import get_template
from app.document.roi import extract_template_field


def extract_portrait_roi(
    image_path,
    output_path=None,
    template_name="ontario_new"
):
    """
    Extract the portrait region from a driver's licence
    using the selected licence template.
    """

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(
            f"Could not load image: {image_path}"
        )

    template = get_template(
        template_name
    )

    field = template["portrait"]

    portrait = extract_template_field(
        image,
        field
    )

    if output_path:
        Path(output_path).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        cv2.imwrite(
            output_path,
            portrait
        )

    return portrait