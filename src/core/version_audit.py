from core.models import DocumentRecord


def build_version_audit(
    records: list[DocumentRecord],
) -> list[dict]:
    """
    Build a version audit report listing each document's
    current revision information.
    """

    results = []

    for record in sorted(records, key=lambda r: r.document_id):
        results.append(
            {
                "Document ID": record.document_id,
                "Version": record.version,
                "Effective Date": record.effective_date,
                "Revision Date": record.revision_date,
                "Owner": record.owner,
            }
        )

    return results