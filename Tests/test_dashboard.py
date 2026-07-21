from pathlib import Path

from core.dashboard import build_dashboard
from core.models import DocumentRecord


def make_record(
    document_id: str,
    missing_references: list[str] | None = None,
) -> DocumentRecord:
    return DocumentRecord(
        file_path=Path(f"{document_id}.docx"),
        file_name=f"{document_id}.docx",
        document_id=document_id,
        missing_references=missing_references or [],
    )


def test_dashboard_metrics():
    records = [
        make_record("DOC-001"),
        make_record("DOC-002", ["DOC-999"]),
        make_record("DOC-003"),
    ]

    health = [
        {"Document ID": "DOC-001", "Health Score": 100},
        {"Document ID": "DOC-002", "Health Score": 90},
        {"Document ID": "DOC-003", "Health Score": 80},
    ]

    diagnostics = [
        {"Severity": "OK"},
        {"Severity": "Warning"},
        {"Severity": "Error"},
    ]

    cross_reference_index = {
        "DOC-001": ["DOC-002", "DOC-003"],
        "DOC-002": ["DOC-003"],
    }

    dashboard = build_dashboard(
        records=records,
        health_results=health,
        diagnostics=diagnostics,
        cross_reference_index=cross_reference_index,
        circular_dependencies=["DOC-010"],
    )

    metrics = {
        row["Metric"]: row["Value"]
        for row in dashboard
    }

    assert metrics["Total Documents"] == 3
    assert metrics["Healthy Documents"] == 1
    assert metrics["Warning Documents"] == 1
    assert metrics["Error Documents"] == 1
    assert metrics["Average Health Score"] == 90.0
    assert metrics["Missing References"] == 1
    assert metrics["Circular Dependencies"] == 1
    assert metrics["Orphan Documents"] == 1
    assert metrics["Cross References"] == 3


def test_empty_dashboard():
    dashboard = build_dashboard(
        records=[],
        health_results=[],
        diagnostics=[],
        cross_reference_index={},
        circular_dependencies=[],
    )

    metrics = {
        row["Metric"]: row["Value"]
        for row in dashboard
    }

    assert metrics["Total Documents"] == 0
    assert metrics["Average Health Score"] == 0
    assert metrics["Cross References"] == 0