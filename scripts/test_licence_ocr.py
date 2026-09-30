from app.document.ocr.tesseract_ocr import (
    read_licence_number
)


IMAGE_PATH = "data/output/licence_number_roi.jpg"


def mask_number(value):
    if not value:
        return "NOT FOUND"

    return (
        value[:2]
        + "*" * (len(value) - 4)
        + value[-2:]
    )


def main():

    print("Reading front licence number...")
    print("-" * 50)

    result = read_licence_number(
        IMAGE_PATH
    )

    print(
        "Found:",
        result["licence_number"] is not None
    )

    print(
        "Licence:",
        mask_number(
            result["licence_number"]
        )
    )

    print(
        "Confidence:",
        result["confidence"]
    )

    print(
        "Agreement:",
        result["agreement"]
    )

    print(
        "Valid attempts:",
        result.get(
            "valid_attempts",
            0
        )
    )


if __name__ == "__main__":
    main()