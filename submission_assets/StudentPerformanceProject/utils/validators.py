"""
utils/validators.py
====================
Reusable input-validation helpers.
"""

from typing import Optional

from utils.logger import get_logger

logger = get_logger(__name__)


def validate_menu_choice(raw_input: str, valid_choices: set[str]) -> Optional[str]:
    """Validate a raw string entered by the user against valid menu options."""
    cleaned = raw_input.strip()
    if cleaned in valid_choices:
        return cleaned

    logger.warning("Invalid menu choice entered: %r", raw_input)
    return None


def validate_positive_float(raw_input: str, field_name: str,
                             minimum: float = 0.0, maximum: Optional[float] = None) -> Optional[float]:
    """Validate that a raw string represents a valid float within an optional range."""
    try:
        value = float(raw_input.strip())
    except ValueError:
        logger.warning("Non-numeric input for %s: %r", field_name, raw_input)
        return None

    if value < minimum or (maximum is not None and value > maximum):
        logger.warning(
            "%s value %.2f out of accepted range [%.2f, %s]",
            field_name, value, minimum, maximum if maximum is not None else "inf"
        )
        return None

    return value


def validate_positive_int(raw_input: str, field_name: str,
                           minimum: int = 0, maximum: Optional[int] = None) -> Optional[int]:
    """Validate that a raw string represents a valid integer within an optional range."""
    try:
        value = int(raw_input.strip())
    except ValueError:
        logger.warning("Non-integer input for %s: %r", field_name, raw_input)
        return None

    if value < minimum or (maximum is not None and value > maximum):
        logger.warning(
            "%s value %d out of accepted range [%d, %s]",
            field_name, value, minimum, maximum if maximum is not None else "inf"
        )
        return None

    return value


def validate_non_empty_string(raw_input: str, field_name: str) -> Optional[str]:
    """Validate that a raw string is non-empty after stripping whitespace."""
    cleaned = raw_input.strip()
    if not cleaned:
        logger.warning("Empty input received for %s", field_name)
        return None
    return cleaned
