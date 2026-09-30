from app.document.ocr.date_ocr import read_dates


IMAGE_PATH = "data/output/licence_number_roi.jpg"


def main():
    print("FRONT DATE OCR")
    print("=" * 50)

    results = read_dates(IMAGE_PATH)

    issue = results["issue"]
    expiry = results["expiry"]

    print("\nISSUE DATE")
    print("-" * 50)
    print("Found:", issue["date"] is not None)
    print("Confidence:", issue["confidence"])
    print("Agreement:", issue["agreement"])

    print("\nEXPIRY DATE")
    print("-" * 50)
    print("Found:", expiry["date"] is not None)
    print("Confidence:", expiry["confidence"])
    print("Agreement:", expiry["agreement"])


if __name__ == "__main__":
    main()