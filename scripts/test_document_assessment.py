from app.document.barcode import (
    decode_barcode,
)

from app.document.barcode_parser import (
    extract_barcode_fields,
)

from app.document.ocr.tesseract_ocr import (
    read_licence_number,
)

from app.document.ocr.date_ocr import (
    read_dates,
)

from app.verification.licence_validator import (
    validate_barcode,
)

from app.verification.document_consistency import (
    check_document_consistency,
)

from app.verification.document_authenticity import (
    assess_local_document,
)


FRONT_ROI = (
    "data/output/licence_number_roi.jpg"
)

BACK_IMAGE = (
    "data/input/licence_back.jpg"
)


def main():
    print("LOCAL DOCUMENT ASSESSMENT")
    print("=" * 50)

    # ------------------------------------------
    # FRONT
    # ------------------------------------------

    front_number_result = read_licence_number(
        FRONT_ROI
    )

    front_dates = read_dates(
        FRONT_ROI
    )

    # ------------------------------------------
    # BACK
    # ------------------------------------------

    barcode_results = decode_barcode(
        BACK_IMAGE
    )

    if not barcode_results:
        print("Barcode could not be decoded.")
        return

    barcode_result = barcode_results[0]

    barcode_text = barcode_result.get(
        "text"
    )

    if not barcode_text:
        print("Barcode detected but contains no decoded text.")
        return

    back_fields = extract_barcode_fields(
        barcode_text
    )
    
    # ------------------------------------------
    # BARCODE VALIDATION
    # ------------------------------------------

    barcode_validation = validate_barcode(
        back_fields
    )

    # ------------------------------------------
    # FRONT / BACK CONSISTENCY
    # ------------------------------------------

    consistency = check_document_consistency(
        front_number=front_number_result.get(
            "licence_number"
        ),
        back_number=back_fields.get(
            "licence_number"
        ),

        front_expiry=front_dates[
            "expiry"
        ].get("date"),
        back_expiry=back_fields.get(
            "expiry_date"
        ),

        front_issue=front_dates[
            "issue"
        ].get("date"),
        back_issue=back_fields.get(
            "issue_date"
        ),

        # Front DOB OCR is currently unreliable.
        front_dob=None,
        back_dob=back_fields.get(
            "date_of_birth"
        ),
    )

    # ------------------------------------------
    # LOCAL ASSESSMENT
    # ------------------------------------------

    assessment = assess_local_document(
        barcode_validation,
        consistency
    )

    # ------------------------------------------
    # RESULTS
    # ------------------------------------------

    print("\nBARCODE")
    print("-" * 50)

    print(
        "Required fields:",
        barcode_validation[
            "required_fields"
        ]["valid"]
    )

    print(
        "Expiry:",
        barcode_validation[
            "expiry"
        ]["status"]
    )

    print(
        "Issue date:",
        barcode_validation[
            "issue_date"
        ]["status"]
    )

    print("\nFRONT/BACK CONSISTENCY")
    print("-" * 50)

    for field, result in consistency[
        "fields"
    ].items():

        print(
            f"{field}: "
            f"{result['status']}"
        )

    print(
        "\nOverall consistency:",
        consistency["status"]
    )

    print("\nLOCAL DOCUMENT ASSESSMENT")
    print("-" * 50)

    print(
        "Status:",
        assessment["status"]
    )

    print(
        "Reason:",
        assessment["reason"]
    )


if __name__ == "__main__":
    main()