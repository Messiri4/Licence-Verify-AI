from app.document.ocr.dob_ocr import read_dob


IMAGE_PATH = "data/output/dob_roi.jpg"


def main():

    print("FRONT DOB OCR")
    print("=" * 50)

    result = read_dob(IMAGE_PATH)

    print(
        "Found:",
        result["date"] is not None
    )

    print(
        "Confidence:",
        result["confidence"]
    )

    print(
        "Agreement:",
        result["agreement"]
    )

    print("\nOCR ATTEMPTS")
    print("-" * 50)

    for attempt in result["attempts"]:
        print(
            attempt["variant"],
            f'| PSM {attempt["psm"]}',
            "| Raw:",
            repr(attempt["raw"]),
            "| Detected:",
            bool(attempt["dates"])
        )


if __name__ == "__main__":
    main()