from core.models import DocumentRecord


def evaluate_document_health(
    records: list[DocumentRecord],
) -> list[dict]:
    """
    Evaluate the health of every document.

    Returns one row per document suitable for exporting.
    """

    results = []

    for record in records:

        score = 100
        issues = []

        if not record.title:
            score -= 10
            issues.append("Missing Title")

        if not record.version:
            score -= 10
            issues.append("Missing Version")

        if not record.owner:
            score -= 10
            issues.append("Missing Owner")

        if record.errors:
            score -= len(record.errors) * 5
            issues.extend(record.errors)

        if record.missing_references:
            score -= len(record.missing_references) * 5
            issues.append(
                f"{len(record.missing_references)} Missing Reference(s)"
            )

        score = max(score, 0)

        results.append(
            {
                "Document ID": record.document_id,
                "Health Score": score,
                "Issues": "; ".join(issues),
            }
        )

    return sorted(
        results,
        key=lambda row: row["Document ID"],
    )