from pathlib import Path

from core.models import DocumentRecord
from core.owner_summary import build_owner_summary


def make_record(
    document_id: str,
    owner: str = "",
) -> DocumentRecord:
    return DocumentRecord(
        file_path=Path(f"{document_id}.docx"),
        file_name=f"{document_id}.docx",
        document_id=document_id,
        owner=owner,
    )


def test_returns_empty_list_when_no_records():
    result = build_owner_summary([])

    assert result == []


def test_counts_documents_by_owner():
    records = [
        make_record("DOC-001", "Operations"),
        make_record("DOC-002", "Finance"),
        make_record("DOC-003", "Operations"),
    ]

    result = build_owner_summary(records)

    assert result == [
        {
            "Owner": "Finance",
            "Document Count": 1,
        },
        {
            "Owner": "Operations",
            "Document Count": 2,
        },
    ]


def test_blank_and_missing_owners_are_unassigned():
    records = [
        make_record("DOC-001"),
        make_record("DOC-002", ""),
        make_record("DOC-003", "   "),
    ]

    result = build_owner_summary(records)

    assert result == [
        {
            "Owner": "Unassigned",
            "Document Count": 3,
        }
    ]


def test_owner_names_are_trimmed():
    records = [
        make_record("DOC-001", " Operations "),
        make_record("DOC-002", "Operations"),
    ]

    result = build_owner_summary(records)

    assert result == [
        {
            "Owner": "Operations",
            "Document Count": 2,
        }
    ]


def test_results_are_sorted_by_owner():
    records = [
        make_record("DOC-001", "Sales"),
        make_record("DOC-002", "Finance"),
        make_record("DOC-003", "Operations"),
    ]

    result = build_owner_summary(records)

    assert [
        row["Owner"]
        for row in result
    ] == [
        "Finance",
        "Operations",
        "Sales",
    ]