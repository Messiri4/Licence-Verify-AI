from app.document.barcode import decode_barcode
from app.document.barcode_parser import extract_licence_number


IMAGE_PATH = "data/input/licence_back.jpg"


def mask(value):
    if not value:
        return "NOT FOUND"

    if len(value) <= 5:
        return "*" * len(value)

    return (
        value[:2]
        + "*" * (len(value) - 4)
        + value[-2:]
    )


def main():

    print("Reading licence barcode...")
    print("-" * 50)

    results = decode_barcode(IMAGE_PATH)

    if not results:
        print("No barcode detected.")
        return

    result = results[0]

    print("Format:", result["format"])
    print("Decoded:", bool(result["text"]))

    licence_number = extract_licence_number(
        result["text"]
    )

    print("\nBARCODE LICENCE NUMBER")
    print("-" * 50)

    if licence_number:
        print("Found: True")
        print("Masked:", mask(licence_number))
        print("Length:", len(licence_number))
    else:
        print("Found: False")


if __name__ == "__main__":
    main()