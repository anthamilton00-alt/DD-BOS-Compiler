from collections import defaultdict

from core.models import DocumentRecord


def find_duplicate_document_ids(
    records: list[DocumentRecord],
) -> list[dict]:
    """
    Detect duplicate Document IDs.

    Returns:
        [
            {
                "Document ID": "ROOM-001",
                "Occurrences": 2,
                "Files": "ROOM-001 A.docx; ROOM-001 B.docx",
            }
        ]
    """

    grouped: dict[str, list[str]] = defaultdict(list)

    for record in records:
        grouped[record.document_id].append(record.file_name)

    duplicates = []

    for document_id in sorted(grouped):
        files = sorted(grouped[document_id])

        if len(files) > 1:
            duplicates.append(
                {
                    "Document ID": document_id,
                    "Occurrences": len(files),
                    "Files": "; ".join(files),
                }
            )

    return duplicates