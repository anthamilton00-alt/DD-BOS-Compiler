from pathlib import Path

from core.coverage import build_reference_coverage
from core.models import DocumentRecord


def make_record(
    document_id: str,
    references: list[str] | None = None,
) -> DocumentRecord:
    return DocumentRecord(
        file_path=Path(f"{document_id}.docx"),
        file_name=f"{document_id}.docx",
        document_id=document_id,
        references=references or [],
    )


def test_returns_empty_list_when_no_records():
    result = build_reference_coverage([], {})

    assert result == []


def test_calculates_inbound_and_outbound_counts():
    records = [
        make_record("DOC-001", ["DOC-002", "DOC-003"]),
        make_record("DOC-002"),
        make_record("DOC-003"),
    ]

    cross_reference_index = {
        "DOC-001": ["DOC-002"],
        "DOC-002": ["DOC-001"],
        "DOC-003": ["DOC-001"],
    }

    result = build_reference_coverage(
        records,
        cross_reference_index,
    )

    assert result == [
        {
            "Document ID": "DOC-001",
            "Inbound References": 1,
            "Outbound References": 2,
            "Total Connections": 3,
        },
        {
            "Document ID": "DOC-002",
            "Inbound References": 1,
            "Outbound References": 0,
            "Total Connections": 1,
        },
        {
            "Document ID": "DOC-003",
            "Inbound References": 1,
            "Outbound References": 0,
            "Total Connections": 1,
        },
    ]


def test_duplicate_outbound_references_are_counted_once():
    records = [
        make_record(
            "DOC-001",
            ["DOC-002", "DOC-002", "doc-002"],
        ),
    ]

    result = build_reference_coverage(
        records,
        {},
    )

    assert result == [
        {
            "Document ID": "DOC-001",
            "Inbound References": 0,
            "Outbound References": 1,
            "Total Connections": 1,
        }
    ]


def test_results_are_sorted_by_document_id():
    records = [
        make_record("DOC-003"),
        make_record("DOC-001"),
        make_record("DOC-002"),
    ]

    result = build_reference_coverage(
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