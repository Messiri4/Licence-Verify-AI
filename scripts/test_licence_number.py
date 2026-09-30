import cv2

from app.document.licence_number import (
    extract_number_roi,
    make_ocr_variants,
)


LICENCE_PATH = "data/output/cropped_licence.jpg"


def main():
    licence = cv2.imread(
        LICENCE_PATH
    )

    if licence is None:
        print(
            f"Could not load: {LICENCE_PATH}"
        )
        return

    roi = extract_number_roi(
        licence
    )

    cv2.imwrite(
        "data/output/licence_number_roi.jpg",
        roi
    )

    variants = make_ocr_variants(
        roi
    )

    for name, image in variants.items():
        path = (
            f"data/output/"
            f"licence_number_{name}.jpg"
        )

        cv2.imwrite(
            path,
            image
        )

        print(
            f"Saved: {path}"
        )

    cv2.imshow(
        "Licence Number ROI",
        roi
    )

    print(
        "Check whether this image contains "
        "the full licence number."
    )

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()