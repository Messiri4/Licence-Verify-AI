from .ontario import ONTARIO_NEW


TEMPLATES = {
    "ontario_new": ONTARIO_NEW,
}


def get_template(template_name):
    """
    Return a licence template by name.
    """

    if template_name not in TEMPLATES:
        raise ValueError(
            f"Unknown licence template: "
            f"{template_name}"
        )

    return TEMPLATES[template_name]