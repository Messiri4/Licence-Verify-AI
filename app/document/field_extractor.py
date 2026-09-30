from app.providers.idanalyzer_provider import (
    scan_licence,
)


def extract_document_fields(
    front_path,
    back_path=None
):
    """
    Primary structured field extraction interface.

    ID Analyzer is currently the primary extractor.
    """

    result = scan_licence(
        front_path,
        back_path
    )

    if not result["success"]:
        return {
            "success": False,
            "source": "idanalyzer",
            "fields": {},
            "decision": result.get(
                "decision"
            ),
            "missing_fields": result.get(
                "missing_fields",
                []
            ),
        }

    return {
        "success": True,
        "source": "idanalyzer",
        "fields": result["fields"],
        "decision": result.get(
            "decision"
        ),
        "missing_fields": result.get(
            "missing_fields",
            []
        ),
    }