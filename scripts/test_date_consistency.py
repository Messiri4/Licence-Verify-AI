from app.document.ocr.date_ocr import read_dates
from app.document.barcode import decode_barcode
from app.document.barcode_parser import extract_barcode_fields
from app.verification.licence_consistency import compare_dates


FRONT_ROI = "data/output/licence_number_roi.jpg"
BACK_IMAGE = "data/input/licence_back.jpg"


def main():
    print("FRONT/BACK DATE CHECK")
    print("=" * 50)

    # Read dates printed on front
    front = read_dates(FRONT_ROI)

    # Decode fields from back
    barcode_results = decode_barcode(BACK_IMAGE)

    if not barcode_results:
        print("Barcode detected: False")
        return

    back = extract_barcode_fields(
        barcode_results[0]["text"]
    )

    # Compare expiry
    expiry_check = compare_dates(
        front["expiry"]["date"],
        back["expiry_date"],
        "expiry date",
    )

    # Compare issue date.
    # This should currently return UNREADABLE rather
    # than incorrectly guessing the issue date.
    issue_check = compare_dates(
        front["issue"]["date"],
        back["issue_date"],
        "issue date",
    )

    print("\nEXPIRY DATE")
    print("-" * 50)
    print("Front confidence:", front["expiry"]["confidence"])
    print("Status:", expiry_check["status"])
    print("Match:", expiry_check["match"])

    print("\nISSUE DATE")
    print("-" * 50)
    print("Front confidence:", front["issue"]["confidence"])
    print("Status:", issue_check["status"])
    print("Match:", issue_check["match"])


if __name__ == "__main__":
    main()