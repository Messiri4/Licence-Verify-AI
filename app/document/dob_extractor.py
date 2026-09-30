import cv2
from pathlib import Path

from app.document.templates import get_template
from app.document.roi import extract_template_field


def extract_dob_roi(
    image_path,
    output_path=None,
    template_name="ontario_new"
):
    """
    Extract the DOB region from a driver's licence
    using the selected licence template.
    """

    image = cv2.imread(image_path)

    if image is None:
        raise FileNotFoundError(
            f"Could not load image: {image_path}"
        )

    # Load the licence template
    template = get_template(
        template_name
    )

    # Get DOB coordinates
    field = template["dob"]

    roi = extract_template_field(
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
            roi
        )

    return roi