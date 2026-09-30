from app.document.field_extractor import (
    extract_document_fields,
)

from app.document.barcode import (
    decode_barcode,
)

from app.document.barcode_parser import (
    extract_barcode_fields,
)

from app.verification.document_consistency import (
    check_document_consistency,
)


FRONT_IMAGE = "data/input/licence_front.jpg"
BACK_IMAGE = "data/input/licence_back.jpg"


def main():
    print("CROSS-SOURCE CONSISTENCY")
    print("=" * 50)

    # ------------------------------------------
    # SOURCE A: ID ANALYZER
    # ------------------------------------------

    id_result = extract_document_fields(
        FRONT_IMAGE,
        BACK_IMAGE
    )

    if not id_result["success"]:
        print("ID Analyzer extraction failed.")
        return

    front_fields = id_result["fields"]

    # ------------------------------------------
    # SOURCE B: LOCAL PDF417
    # ------------------------------------------

    barcode_results = decode_barcode(
        BACK_IMAGE
    )

    if not barcode_results:
        print("PDF417 barcode could not be decoded.")
        return

    barcode_text = barcode_results[0].get(
        "text"
    )

    if not barcode_text:
        print("PDF417 contains no decoded data.")
        return

    back_fields = extract_barcode_fields(
        barcode_text
    )

    # ------------------------------------------
    # CROSS-SOURCE COMPARISON
    # ------------------------------------------

    consistency = check_document_consistency(
        front_number=front_fields.get(
            "licence_number"
        ),
        back_number=back_fields.get(
            "licence_number"
        ),

        front_dob=front_fields.get(
            "date_of_birth"
        ),
        back_dob=back_fields.get(
            "date_of_birth"
        ),

        front_issue=front_fields.get(
            "issue_date"
        ),
        back_issue=back_fields.get(
            "issue_date"
        ),

        front_expiry=front_fields.get(
            "expiry_date"
        ),
        back_expiry=back_fields.get(
            "expiry_date"
        ),
    )

    # ------------------------------------------
    # SAFE RESULTS
    # ------------------------------------------

    print("\nSOURCES")
    print("-" * 50)
    print("Source A: ID Analyzer")
    print("Source B: Local PDF417")

    print("\nFIELD COMPARISON")
    print("-" * 50)

    labels = {
        "licence_number": "Licence number",
        "date_of_birth": "DOB",
        "issue_date": "Issue date",
        "expiry_date": "Expiry date",
    }

    for field, result in consistency[
        "fields"
    ].items():

        print(
            f"{labels[field]}: "
            f"{result['status']}"
        )

    print("\nOVERALL")
    print("-" * 50)

    print(
        "Status:",
        consistency["status"]
    )

    if consistency["mismatches"]:
        print(
            "Mismatches:",
            ", ".join(
                consistency["mismatches"]
            )
        )

    if consistency["unreadable_fields"]:
        print(
            "Unavailable fields:",
            ", ".join(
                consistency[
                    "unreadable_fields"
                ]
            )
        )


if __name__ == "__main__":
    main()