from app.providers.idanalyzer_provider import (
    scan_licence,
)


FRONT_IMAGE = (
    "data/input/licence_front.jpg"
)

BACK_IMAGE = (
    "data/input/licence_back.jpg"
)


def main():

    print("ID ANALYZER TEST")
    print("=" * 50)

    print(
        "Sending licence for OCR..."
    )

    result = scan_licence(
        FRONT_IMAGE,
        BACK_IMAGE
    )

    print(
        "\nScan completed."
    )

    print("\nTOP-LEVEL RESPONSE FIELDS")
    print("-" * 50)

    for key in result.keys():
        print(key)

    print("\nIMPORTANT FIELD CHECK")
    print("-" * 50)

    data = result.get("data", {})

    print("\nID ANALYZER FIELD TYPES")
    print("-" * 50)

    important_fields = [
        "documentNumber",
        "dob",
        "issued",
        "expiry",
    ]

    for field in important_fields:
        value = data.get(field)

        print(
            f"\n{field}"
        )

        print(
            "Type:",
            type(value).__name__
        )

        if isinstance(value, list):
            print(
                "List length:",
                len(value)
            )

            if value:
                print(
                    "First item type:",
                    type(value[0]).__name__
                )

                if isinstance(
                    value[0],
                    dict
                ):
                    print(
                        "Dictionary keys:",
                        list(
                            value[0].keys()
                        )
                    )

        elif isinstance(value, dict):
            print(
                "Dictionary keys:",
                list(value.keys())
            )

    fields = [
        "documentName",
        "documentType",
        "documentNumber",
        "countryFull",
        "stateFull",
        "dob",
        "issued",
        "expiry",
        "firstName",
        "lastName",
        "vehicleClass",
    ]

    for field in fields:
        value = data.get(field)

        print(
            f"{field}:",
            "FOUND"
            if value not in (None, "")
            else "NOT FOUND"
        )


    print("\nID ANALYZER RESULT")
    print("-" * 50)

    print(
        "Success:",
        result.get("success")
    )

    print(
        "Decision:",
        result.get("decision")
    )

    print(
        "Missing fields:",
        result.get("missingFields")
    )

    print(
        "Credits remaining:",
        result.get("credit")
    )


if __name__ == "__main__":
    main()