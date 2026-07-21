from core.models import DocumentRecord


def build_change_impact(
    records: list[DocumentRecord],
    cross_reference_index: dict[str, list[str]],
) -> list[dict]:
    """
    Build a change impact report.

    The impact count is the number of documents that directly
    reference a given document. A higher count means changes to
    that document may affect more of the operating system.
    """

    results = []

    for record in sorted(records, key=lambda r: r.document_id):
        impacted_by = sorted(
            cross_reference_index.get(record.document_id, [])
        )

        results.append(
            {
                "Document ID": record.document_id,
                "Dependent Documents": "; ".join(impacted_by),
                "Impact Count": len(impacted_by),
            }
        )

    return results