from core.models import DocumentRecord


def build_risk_scores(
    records: list[DocumentRecord],
    health_results: dict[str, int],
    inbound_reference_counts: dict[str, int],
) -> list[dict]:
    """
    Build a simple governance risk score for each document.

    Risk Score =
        Health Issues + Inbound References

    Documents with many health issues and many inbound
    references represent higher governance risk because
    they are both problematic and widely depended upon.
    """

    results = []

    for record in sorted(records, key=lambda r: r.document_id):
        health = health_results.get(record.document_id, 0)
        inbound = inbound_reference_counts.get(record.document_id, 0)

        results.append(
            {
                "Document ID": record.document_id,
                "Health Issues": health,
                "Inbound References": inbound,
                "Risk Score": health + inbound,
            }
        )

    return results