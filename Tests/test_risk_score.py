from pathlib import Path

from core.models import DocumentRecord
from core.risk_score import build_risk_scores


def make_record(document_id: str) -> DocumentRecord:
    return DocumentRecord(
        file_path=Path(f"{document_id}.docx"),
        file_name=f"{document_id}.docx",
        document_id=document_id,
    )


def test_returns_empty_list_when_no_records():
    result = build_risk_scores([], {}, {})

    assert result == []


def test_builds_risk_scores():
    records = [
        make_record("DOC-001"),
        make_record("DOC-002"),
    ]

    health_results = {
        "DOC-001": 2,
        "DOC-002": 0,
    }

    inbound_reference_counts = {
        "DOC-001": 5,
        "DOC-002": 1,
    }

    result = build_risk_scores(
        records,
        health_results,
        inbound_reference_counts,
    )

    assert result == [
        {
            "Document ID": "DOC-001",
            "Health Issues": 2,
            "Inbound References": 5,
            "Risk Score": 7,
        },
        {
            "Document ID": "DOC-002",
            "Health Issues": 0,
            "Inbound References": 1,
            "Risk Score": 1,
        },
    ]


def test_missing_values_default_to_zero():
    records = [
        make_record("DOC-001"),
    ]

    result = build_risk_scores(
        records,
        {},
        {},
    )

    assert result == [
        {
            "Document ID": "DOC-001",
            "Health Issues": 0,
            "Inbound References": 0,
            "Risk Score": 0,
        }
    ]


def test_results_are_sorted_by_document_id():
    records = [
        make_record("DOC-003"),
        make_record("DOC-001"),
        make_record("DOC-002"),
    ]

    result = build_risk_scores(
        records,
        {},
        {},
    )

    assert [
        row["Document ID"]
        for row in result
    ] == [
        "DOC-001",
        "DOC-002",
        "DOC-003",
    ]