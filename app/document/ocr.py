import easyocr

reader = easyocr.Reader(["en"])


def extract_text(image_path: str):
    results = reader.readtext(image_path)

    extracted_text = []

    for bbox, text, confidence in results:
        extracted_text.append({
            "text": text,
            "confidence": float(confidence)
        })

    return extracted_text