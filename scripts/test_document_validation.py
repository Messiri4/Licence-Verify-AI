from app.document.field_extractor import (
    extract_document_fields,
)

from app.verification.licence_validator import (
    validate_document,
)


FRONT_IMAGE = "data/input/licence_front.jpg"
BACK_IMAGE = "data/input/licence_back.jpg"


def main():
    print("DOCUMENT VALIDATION")
    print("=" * 50)

    extraction = extract_document_fields(
        FRONT_IMAGE,
        BACK_IMAGE
    )

    if not extraction["success"]:
        print("Field extraction failed.")
        return

    fields = extraction["fields"]

    print("\nDATE FORMAT DEBUG")
    print("-" * 50)

    for field in [
        "date_of_birth",
        "issue_date",
        "expiry_date",
    ]:
        value = fields.get(field)

        if value is None:
            print(
                f"{field}: NONE"
            )
            continue

        value = str(value)

        masked = "".join(
            char if not char.isdigit() else "#"
            for char in value
        )

        print(
            f"{field}: "
            f"type={type(fields.get(field)).__name__}, "
            f"length={len(value)}, "
            f"pattern={masked}"
        )

    validation = validate_document(
        extraction["fields"]
    )

    labels = {
        "required_fields": "Required fields",
        "licence_number": "Ontario number format",
        "expiry": "Expiry",
        "issue_date": "Issue date",
        "date_of_birth": "DOB",
        "jurisdiction": "Jurisdiction",
    }

    print("\nCHECKS")
    print("-" * 50)

    for name, result in validation[
        "checks"
    ].items():
        print(
            f"{labels[name]}: "
            f"{result['status']}"
        )

    print("\nOVERALL")
    print("-" * 50)

    print(
        "Status:",
        validation["status"]
    )


if __name__ == "__main__":
    main()