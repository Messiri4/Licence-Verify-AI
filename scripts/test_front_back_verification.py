from app.document.ocr.tesseract_ocr import (
    read_licence_number
)

from app.document.barcode import (
    decode_barcode
)

from app.document.barcode_parser import (
    extract_licence_number
)

from app.verification.licence_consistency import (
    compare_licence_numbers
)


FRONT_ROI = "data/output/licence_number_roi.jpg"
BACK_IMAGE = "data/input/licence_back.jpg"


def mask(value):
    if not value:
        return "NOT FOUND"

    return (
        value[:2]
        + "*" * (len(value) - 4)
        + value[-2:]
    )


def main():

    print("FRONT/BACK LICENCE CHECK")
    print("=" * 50)

    # -------------------------
    # FRONT
    # -------------------------

    front_result = read_licence_number(
        FRONT_ROI
    )

    front_number = front_result[
        "licence_number"
    ]

    print("\nFRONT OCR")
    print("-" * 50)

    print(
        "Number:",
        mask(front_number)
    )

    print(
        "Confidence:",
        front_result["confidence"]
    )

    print(
        "Agreement:",
        front_result["agreement"]
    )

    # -------------------------
    # BACK
    # -------------------------

    barcode_results = decode_barcode(
        BACK_IMAGE
    )

    back_number = None

    if barcode_results:
        back_number = extract_licence_number(
            barcode_results[0]["text"]
        )

    print("\nBACK PDF417")
    print("-" * 50)

    print(
        "Number:",
        mask(back_number)
    )

    # -------------------------
    # COMPARE
    # -------------------------

    comparison = compare_licence_numbers(
        front_number,
        back_number
    )

    print("\nCONSISTENCY CHECK")
    print("-" * 50)

    print(
        "Status:",
        comparison["status"]
    )

    print(
        "Match:",
        comparison["match"]
    )

    print(
        "Reason:",
        comparison["reason"]
    )


if __name__ == "__main__":
    main()