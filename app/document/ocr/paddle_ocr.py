from paddleocr import PaddleOCR


ocr = PaddleOCR(
    lang="en",
    use_doc_orientation_classify=False,
    use_doc_unwarping=False,
    use_textline_orientation=False
)


def read_text(image_path):
    results = ocr.predict(image_path)

    extracted = []

    for result in results:
        extracted.append(result)

    return extracted