from core.models import DocumentRecord


def build_diagnostics(records: list[DocumentRecord]) -> list[dict]:
    """
    Build a diagnostics report summarizing warnings and errors
    for each document.
    """

    diagnostics = []

    for record in sorted(records, key=lambda r: r.document_id):

        severity = "OK"

        if record.errors:
            severity = "Error"
        elif record.missing_references:
            severity = "Warning"

        diagnostics.append(
            {
                "Document ID": record.document_id,
                "Severity": severity,
                "Error Count": len(record.errors),
                "Missing References": len(record.missing_references),
                "Message": "; ".join(
                    record.errors
                    + (
                        [f"{len(record.missing_references)} Missing Reference(s)"]
                        if record.missing_references
                        else []
                    )
                ),
            }
        )

    return diagnostics