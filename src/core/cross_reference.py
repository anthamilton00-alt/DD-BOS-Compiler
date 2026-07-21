from collections import defaultdict

from core.models import DocumentRecord


def build_cross_reference_index(
    records: list[DocumentRecord],
) -> dict[str, list[str]]:
    """
    Build a reverse-reference index.

    Returns:
        {
            "ROOM-001": ["FP-0001", "DD-007"],
            "DD-007": ["ASM-202"],
        }

    Meaning:
        Key document is referenced by the listed documents.
    """

    document_ids = {
        record.document_id
        for record in records
    }

    index: dict[str, set[str]] = defaultdict(set)

    for record in records:
        for reference in record.references:
            reference = reference.upper()

            if reference in document_ids:
                index[reference].add(record.document_id)

    return {
        document: sorted(referrers)
        for document, referrers in sorted(index.items())
    }