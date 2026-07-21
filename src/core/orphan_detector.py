from core.models import DocumentRecord


def find_orphan_documents(
    records: list[DocumentRecord],
    cross_reference_index: dict[str, list[str]],
) -> list[dict]:
    """
    Detect documents that are never referenced by any other
    document.

    Returns:
        [
            {
                "Document ID": "HR-004",
                "Title": "...",
                "Owner": "...",
            }
        ]
    """

    orphans = []

    for record in sorted(records, key=lambda r: r.document_id):

        if record.document_id not in cross_reference_index:

            orphans.append(
                {
                    "Document ID": record.document_id,
                    "Title": record.title,
                    "Owner": record.owner,
                }
            )

    return orphans