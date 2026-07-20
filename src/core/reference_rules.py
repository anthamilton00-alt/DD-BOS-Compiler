import re

DOCUMENT_ID_PATTERN = re.compile(
    r"^(ASM|DD|ROOM|FP|LAB|PROD)-\d+$",
    re.IGNORECASE,
)


def classify_reference(reference: str, known_document_ids: set[str]) -> tuple[bool, str]:
    """
    Classify a document reference.

    Returns:
        (exists, status)
    """

    reference = reference.upper()

    if reference in known_document_ids:
        return True, "Resolved"

    if DOCUMENT_ID_PATTERN.fullmatch(reference):
        return False, "Expected"

    return False, "Invalid"