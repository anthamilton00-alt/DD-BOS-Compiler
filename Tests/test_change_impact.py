from pathlib import Path

from core.change_impact import build_change_impact
from core.models import DocumentRecord


def make_record(document_id: str) -> DocumentRecord:
    return DocumentRecord(
        file_path=Path(f"{document_id}.docx"),
        file_name=f"{document_id}.docx",
        document_id=document_id,
    )


def test_returns_empty_list_when_no_records():
    result = build_change_impact([], {})

    assert result == []


def test_builds_change_impact_report():
    records = [
        make_record("DOC-001"),
        make_record("DOC-002"),
        make_record("DOC-003"),
    ]

    cross_reference_index = {
        "DOC-001": ["DOC-003", "DOC-002"],
        "DOC-003": ["DOC-001"],
    }

    result = build_change_impact(
        records,
        cross_reference_index,
    )

    assert result == [
        {
            "Document ID": "DOC-001",
            "Dependent Documents": "DOC-002; DOC-003",
            "Impact Count": 2,
        },
        {
            "Document ID": "DOC-002",
            "Dependent Documents": "",
            "Impact Count": 0,
        },
        {
            "Document ID": "DOC-003",
            "Dependent Documents": "DOC-001",
            "Impact Count": 1,
        },
    ]


def test_handles_documents_with_no_dependents():
    records = [
        make_record("DOC-001"),
    ]

    result = build_change_impact(
        records,
        {},
    )

    assert result == [
        {
            "Document ID": "DOC-001",
            "Dependent Documents": "",
            "Impact Count": 0,
        }
    ]


def test_results_are_sorted_by_document_id():
    records = [
        make_record("DOC-003"),
        make_record("DOC-001"),
        make_record("DOC-002"),
    ]

    result = build_change_impact(
        records,
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