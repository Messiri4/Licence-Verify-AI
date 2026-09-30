from app.document.ocr.paddle_ocr import read_text


IMAGE_PATH = (
    "data/output/licence_number_roi.jpg"
)


def main():
    print(
        "Running PaddleOCR..."
    )

    results = read_text(
        IMAGE_PATH
    )

    print("\nRAW RESULT")
    print("=" * 60)

    for result in results:
        print(result)


if __name__ == "__main__":
    main()