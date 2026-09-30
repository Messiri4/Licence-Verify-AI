import cv2
import easyocr

from app.document.licence_number import (
    make_ocr_variants,
    normalize_licence_number,
    is_valid_ontario_format,
)


IMAGE_PATH = "data/output/licence_number_roi.jpg"


def main():

    print("1. Loading licence-number image...")

    image = cv2.imread(IMAGE_PATH)

    if image is None:
        print(f"Could not load: {IMAGE_PATH}")
        return

    print("2. Image loaded.")
    print("3. Loading EasyOCR...")

    reader = easyocr.Reader(
        ["en"],
        gpu=False,
        verbose=True
    )

    print("4. EasyOCR loaded.")

    variants = make_ocr_variants(image)

    print("\nLICENCE NUMBER OCR")
    print("=" * 60)

    for name, variant in variants.items():

        print(f"\nProcessing {name}...")

        results = reader.readtext(
            variant,
            detail=1,
            paragraph=False,
            allowlist=(
                "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                "0123456789- "
            )
        )

        print(name.upper())
        print("-" * 60)

        if not results:
            print("No text detected.")
            continue

        for _, text, confidence in results:

            normalized = normalize_licence_number(
                text
            )

            valid = is_valid_ontario_format(
                text
            )

            print(f"Raw:         {text}")
            print(f"Normalized:  {normalized}")
            print(f"Confidence:  {confidence:.3f}")
            print(f"Valid format: {valid}")


if __name__ == "__main__":
    main()