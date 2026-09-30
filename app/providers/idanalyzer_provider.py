import os

from dotenv import load_dotenv
from idanalyzer2 import Scanner


load_dotenv()


def create_scanner():
    """
    Create an ID Analyzer scanner using the
    API key stored in .env.
    """

    api_key = os.getenv(
        "IDANALYZER_KEY"
    )

    if not api_key:
        raise ValueError(
            "IDANALYZER_KEY was not found "
            "in the .env file."
        )

    scanner = Scanner(
        api_key
    )

    scanner.throwApiException(
        True
    )

    return scanner

def normalize_provider_value(value):
    """
    Extract the actual value from an ID Analyzer
    field and return a simple scalar value.
    """

    if value is None:
        return None

    # ID Analyzer may return multiple candidates.
    if isinstance(value, list):
        if not value:
            return None

        value = value[0]

    # ID Analyzer field objects contain the
    # extracted value plus confidence/box metadata.
    if isinstance(value, dict):
        return value.get("value")

    return value

def scan_licence(
    front_path,
    back_path=None
):
    """
    Extract structured driver's-licence fields
    using ID Analyzer.

    ID Analyzer is the primary front-side
    document field extractor.
    """

    scanner = create_scanner()

    result = scanner.quickScan(
        front_path,
        back_path,
        False
    )

    if not result.get("success"):
        return {
            "success": False,
            "fields": {},
            "decision": result.get("decision"),
            "missing_fields": result.get(
                "missingFields",
                []
            ),
        }

    data = result.get("data", {})

    fields = {
        "licence_number": normalize_provider_value(
            data.get("documentNumber")
        ),

        "date_of_birth": normalize_provider_value(
            data.get("dob")
        ),

        "issue_date": normalize_provider_value(
            data.get("issued")
        ),

        "expiry_date": normalize_provider_value(
            data.get("expiry")
        ),

        "document_type": normalize_provider_value(
            data.get("documentType")
        ),

        "document_name": normalize_provider_value(
            data.get("documentName")
        ),

        "country": normalize_provider_value(
            data.get("countryFull")
        ),

        "province": normalize_provider_value(
            data.get("stateShort")
            or data.get("stateFull")
        ),

        "vehicle_class": normalize_provider_value(
            data.get("vehicleClass")
        ),
    }

    return {
        "success": True,
        "fields": fields,
        "decision": result.get(
            "decision"
        ),
        "missing_fields": result.get(
            "missingFields",
            []
        ),
        "review_score": result.get(
            "reviewScore"
        ),
        "reject_score": result.get(
            "rejectScore"
        ),
    }