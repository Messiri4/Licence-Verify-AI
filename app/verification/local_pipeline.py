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

from app.verification.licence_validator import (
    validate_document,
)

from app.verification.local_assessment import (
    assess_local_verification,
)


def _value(field):
    """
    Extract the actual value from an ID Analyzer
    normalized field.

    ID Analyzer fields may look like:
    {
        "value": "...",
        "confidence": ...,
        ...
    }
    """

    if isinstance(field, dict):
        return field.get("value")

    return field


def run_local_verification(
    front_path,
    back_path,
    identity_verification=None,
):
    """
    Run Stages 3-8 of the local verification pipeline.

    This pipeline does NOT check official MTO status.
    """

    # ==========================================
    # FRONT FIELD EXTRACTION
    # ==========================================

    extraction = extract_document_fields(
        front_path,
        back_path,
    )

    if not extraction.get("success"):
        return {
            "status": "UNKNOWN",
            "stage": "FIELD_EXTRACTION",
            "reason": "Front document field extraction failed.",
            "official_licence_status": "NOT_CHECKED",
        }

    raw_front_fields = extraction.get(
        "fields",
        {},
    )

    # Flatten normalized ID Analyzer fields.
    front_fields = {
        key: _value(value)
        for key, value in raw_front_fields.items()
    }

    # ==========================================
    # BACK PDF417
    # ==========================================

    barcode_results = decode_barcode(
        back_path
    )

    if not barcode_results:
        return {
            "status": "PARTIAL",
            "stage": "PDF417",
            "reason": "Back PDF417 barcode could not be decoded.",
            "front_fields": front_fields,
            "official_licence_status": "NOT_CHECKED",
        }

    barcode_result = barcode_results[0]

    barcode_text = barcode_result.get(
        "text"
    )

    if not barcode_text:
        return {
            "status": "PARTIAL",
            "stage": "PDF417",
            "reason": "PDF417 barcode contained no decoded text.",
            "front_fields": front_fields,
            "official_licence_status": "NOT_CHECKED",
        }

    back_fields = extract_barcode_fields(
        barcode_text
    )

    # ==========================================
    # STAGE 5 — CROSS-SOURCE CONSISTENCY
    # ==========================================

    consistency = check_document_consistency(
        front_number=front_fields.get(
            "licence_number"
        ),
        back_number=back_fields.get(
            "licence_number"
        ),

        front_expiry=front_fields.get(
            "expiry_date"
        ),
        back_expiry=back_fields.get(
            "expiry_date"
        ),

        front_issue=front_fields.get(
            "issue_date"
        ),
        back_issue=back_fields.get(
            "issue_date"
        ),

        front_dob=front_fields.get(
            "date_of_birth"
        ),
        back_dob=back_fields.get(
            "date_of_birth"
        ),
    )

    # ==========================================
    # STAGE 6 — DOCUMENT VALIDATION
    # ==========================================

    document_validation = validate_document(
        front_fields
    )

    # ==========================================
    # STAGE 7 — IDENTITY VERIFICATION
    # ==========================================
    #
    # Passed into this function because the
    # interactive webcam/liveness session occurs
    # separately.
    #
    # DEVELOPMENT MODE:
    # The current reference identity may be the
    # developer test identity rather than the
    # actual licence portrait.
    #

    # ==========================================
    # STAGE 8 — LOCAL ASSESSMENT
    # ==========================================

    assessment = assess_local_verification(
        consistency=consistency,
        document_validation=document_validation,
        identity_verification=identity_verification,
    )

    return {
        "status": assessment["status"],

        "extraction": {
            "success": extraction["success"],
            "source": extraction.get("source"),
            "decision": extraction.get("decision"),
        },

        "front_fields": front_fields,
        "back_fields": back_fields,

        "consistency": consistency,
        "document_validation": document_validation,
        "identity_verification": identity_verification,

        "assessment": assessment,

        # Stage 9 has not run.
        "official_licence_status": "NOT_CHECKED",
    }