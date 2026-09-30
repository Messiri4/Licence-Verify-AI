from enum import Enum


class OfficialLicenceStatus(str, Enum):
    """
    Possible results from an official licence-status
    provider.

    These values must never be inferred from local
    document or identity verification.
    """

    VALID = "VALID"
    INVALID = "INVALID"
    SUSPENDED = "SUSPENDED"
    CANCELLED = "CANCELLED"
    EXPIRED = "EXPIRED"

    NOT_CHECKED = "NOT_CHECKED"
    UNAVAILABLE = "UNAVAILABLE"
    ERROR = "ERROR"


def get_official_licence_status(
    licence_number,
):
    """
    Stage 9 — Official licence status.

    IMPORTANT:
    This function does NOT currently contact MTO.

    The Ontario Driver's Licence Check is the
    authoritative external service, but this
    application currently has no configured
    authorized programmatic MTO integration.

    Local verification results must never be used
    to manufacture an official licence status.
    """

    if not licence_number:
        return {
            "status": OfficialLicenceStatus.ERROR.value,
            "source": "MTO",
            "official": False,
            "checked": False,
            "reason": (
                "No licence number was supplied "
                "for official verification."
            ),
        }

    return {
        "status": OfficialLicenceStatus.NOT_CHECKED.value,
        "source": "MTO",
        "official": False,
        "checked": False,
        "reason": (
            "Official MTO status has not been checked. "
            "No authorized programmatic MTO integration "
            "is currently configured."
        ),
    }