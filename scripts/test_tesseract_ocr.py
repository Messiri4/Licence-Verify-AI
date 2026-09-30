from app.document.ocr.tesseract_ocr import (
    read_text_candidates
)

from app.document.licence_number import (
    normalize_licence_number,
    is_valid_ontario_format,
)


IMAGE_PATH = (
    "data/output/licence_number_roi.jpg"
)


def main():
    print("Running Tesseract OCR...\n")

    results = read_text_candidates(
        IMAGE_PATH
    )

    for result in results:

        text = result["text"]

        normalized = (
            normalize_licence_number(
                text
            )
        )

        valid = (
            is_valid_ontario_format(
                normalized
            )
        )

        print(
            f"{result['variant']} "
            f"| PSM {result['psm']}"
        )

        print(
            f"Raw:        {text}"
        )

        print(
            f"Normalized: {normalized}"
        )

        print(
            f"Valid:      {valid}"
        )

        print("-" * 50)


if __name__ == "__main__":
    main()