"""
Ontario driver's licence front-side template.

Coordinates are normalized relative to the
cropped/normalized licence image.

Each field uses:
    x1, y1 = top-left corner
    x2, y2 = bottom-right corner
"""

ONTARIO_NEW = {
    "name": "ontario_new",

    # Working licence-number region
    "licence_number": {
        "x1": 0.38,
        "y1": 0.43,
        "x2": 0.99,
        "y2": 0.58,
    },

    # Working portrait region
    "portrait": {
        "x1": 0.03,
        "y1": 0.23,
        "x2": 0.34,
        "y2": 0.82,
    },

    # DOB region
    "dob": {
        "x1": 0.00,
        "y1": 0.82,
        "x2": 0.48,
        "y2": 1.00,
    },
}