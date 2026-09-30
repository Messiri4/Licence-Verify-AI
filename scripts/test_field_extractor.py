from app.document.field_extractor import (
    extract_document_fields,
)


FRONT_IMAGE = (
    "data/input/licence_front.jpg"
)

BACK_IMAGE = (
    "data/input/licence_back.jpg"
)


def main():
    print("PRIMARY FIELD EXTRACTOR")
    print("=" * 50)

    result = extract_document_fields(
        FRONT_IMAGE,
        BACK_IMAGE
    )

    print(
        "Success:",
        result["success"]
    )

    print(
        "Source:",
        result["source"]
    )

    print(
        "Decision:",
        result.get("decision")
    )

    print("\nFIELDS")
    print("-" * 50)

    fields = result.get(
        "fields",
        {}
    )

    for name, value in fields.items():
        print(
            f"{name}:",
            "FOUND"
            if value not in (None, "")
            else "NOT FOUND"
        )


if __name__ == "__main__":
    main()