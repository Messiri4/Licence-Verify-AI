from app.document.barcode import decode_barcode
from app.document.barcode_parser import extract_barcode_fields
from app.verification.licence_validator import validate_barcode


BACK_IMAGE = "data/input/licence_back.jpg"


def main():

    print("LICENCE VALIDATION")
    print("=" * 50)

    results = decode_barcode(BACK_IMAGE)

    if not results:
        print("Barcode detected: False")
        return

    raw_text = results[0]["text"]

    fields = extract_barcode_fields(raw_text)

    validation = validate_barcode(fields)

    print("Barcode detected: True")

    print(
        "Required fields:",
        "PASS"
        if validation["required_fields"]["valid"]
        else "FAIL"
    )

    if not validation["required_fields"]["valid"]:
        print(
            "Missing fields:",
            validation["required_fields"]["missing_fields"]
        )

    print(
        "Expiry:",
        validation["expiry"]["status"]
    )

    print(
        "Expiry check:",
        "PASS"
        if validation["expiry"]["valid"]
        else "FAIL"
    )

    print(
    "Issue date:",
    validation["issue_date"]["status"]
    )

    print(
        "Issue date check:",
        "PASS"
        if validation["issue_date"]["valid"]
        else "FAIL"
    )


if __name__ == "__main__":
    main()