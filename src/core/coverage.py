from core.models import DocumentRecord


def build_reference_coverage(
    records: list[DocumentRecord],
    cross_reference_index: dict[str, list[str]],
) -> list[dict]:
    """
    Build inbound/outbound reference metrics for every document.

    Returns:
        [
            {
                "Document ID": "...",
                "Inbound References": 2,
                "Outbound References": 5,
                "Total Connections": 7,
            }
        ]
    """

    coverage = []

    for record in sorted(records, key=lambda r: r.document_id):

        inbound = len(
            cross_reference_index.get(
                record.document_id,
                [],
            )
        )

        outbound = len(
            {
                reference.upper()
                for reference in record.references
            }
        )

        coverage.append(
            {
                "Document ID": record.document_id,
                "Inbound References": inbound,
                "Outbound References": outbound,
                "Total Connections": inbound + outbound,
            }
        )

    return coverage