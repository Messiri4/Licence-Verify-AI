from pathlib import Path

import cv2

from app.document.detector import (
    detect_licence
)
from app.document.cropper import (
    crop_licence
)
from app.document.licence_number import (
    extract_number_roi
)

from app.document.detector import (
    detect_licence,
    draw_detection
)




def main():
    image_path = (
        Path("data/input/licence_front.jpg")
    )

    print("Detecting licence...")

    detection = detect_licence(
        image_path
    )

    if detection is None:
        print(
            "No driver's licence detected."
        )
        return

    print(
        "Licence detected:",
        round(
            detection["confidence"],
            3
        )
    )

    # ------------------------------
    # Visualize detection
    # ------------------------------


    visualization = draw_detection(
        image_path,
        detection
    )

    cv2.imwrite(
        "data/output/licence_detection.jpg",
        visualization
    )

    cv2.imshow(
        "Licence Detection",
        visualization
    )

    print(
        "Press any key on the image window "
        "to continue..."
    )

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # ------------------------------
    # Crop licence
    # ------------------------------

    licence = crop_licence(
            str(image_path),
            detection
        )
    
    cv2.imwrite(
        "data/output/cropped_licence.jpg",
        licence
    )

    # ------------------------------
    # Licence number region
    # ------------------------------

    number_roi = (
            extract_number_roi(
                licence
            )
        )
    
    cv2.imwrite(
        "data/output/licence_number.jpg",
        number_roi
    )

    print(
        "Licence processing complete."
    )


if __name__ == "__main__":
    main()