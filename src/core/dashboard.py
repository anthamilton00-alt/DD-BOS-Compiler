from core.models import DocumentRecord


def build_dashboard(
    records: list[DocumentRecord],
    health_results: list[dict],
    diagnostics: list[dict],
    cross_reference_index: dict[str, list[str]],
    circular_dependencies: list[str],
) -> list[dict]:
    """
    Build the executive dashboard summary.
    """

    total_documents = len(records)

    healthy_documents = sum(
        1
        for row in diagnostics
        if row["Severity"] == "OK"
    )

    warning_documents = sum(
        1
        for row in diagnostics
        if row["Severity"] == "Warning"
    )

    error_documents = sum(
        1
        for row in diagnostics
        if row["Severity"] == "Error"
    )

    average_health = (
        round(
            sum(
                row["Health Score"]
                for row in health_results
            ) / total_documents,
            1,
        )
        if total_documents
        else 0
    )

    missing_references = sum(
        len(record.missing_references)
        for record in records
    )

    orphan_documents = sum(
        1
        for record in records
        if record.document_id not in cross_reference_index
    )

    return [
        {"Metric": "Total Documents", "Value": total_documents},
        {"Metric": "Healthy Documents", "Value": healthy_documents},
        {"Metric": "Warning Documents", "Value": warning_documents},
        {"Metric": "Error Documents", "Value": error_documents},
        {"Metric": "Average Health Score", "Value": average_health},
        {"Metric": "Missing References", "Value": missing_references},
        {"Metric": "Circular Dependencies", "Value": len(circular_dependencies)},
        {"Metric": "Orphan Documents", "Value": orphan_documents},
        {"Metric": "Cross References", "Value": sum(len(v) for v in cross_reference_index.values())},
    ]