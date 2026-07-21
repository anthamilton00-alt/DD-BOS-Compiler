from pathlib import Path

from core.models import DocumentRecord
from core.version_audit import build_version_audit


def make_record(
    document_id: str,
    version: str = "",
    effective_date: str = "",
    revision_date: str = "",
    owner: str = "",
) -> DocumentRecord:
    return DocumentRecord(
        file_path=Path(f"{document_id}.docx"),
        file_name=f"{document_id}.docx",
        document_id=document_id,
        version=version,
        effective_date=effective_date,
        revision_date=revision_date,
        owner=owner,
    )


def test_returns_empty_list_when_no_records():
    result = build_version_audit([])

    assert result == []


def test_builds_version_audit():
    records = [
        make_record(
            "DOC-001",
            version="1.0",
            effective_date="2025-01-01",
            revision_date="2026-01-01",
            owner="Operations",
        ),
        make_record(
            "DOC-002",
            version="2.3",
            effective_date="2025-03-15",
            revision_date="2026-03-15",
            owner="Finance",
        ),
    ]

    result = build_version_audit(records)

    assert result == [
        {
            "Document ID": "DOC-001",
            "Version": "1.0",
            "Effective Date": "2025-01-01",
            "Revision Date": "2026-01-01",
            "Owner": "Operations",
        },
        {
            "Document ID": "DOC-002",
            "Version": "2.3",
            "Effective Date": "2025-03-15",
            "Revision Date": "2026-03-15",
            "Owner": "Finance",
        },
    ]


def test_missing_fields_default_to_empty_strings():
    records = [
        make_record("DOC-001"),
    ]

    result = build_version_audit(records)

    assert result == [
        {
            "Document ID": "DOC-001",
            "Version": "",
            "Effective Date": "",
            "Revision Date": "",
            "Owner": "",
        }
    ]


def test_results_are_sorted_by_document_id():
    records = [
        make_record("DOC-003"),
        make_record("DOC-001"),
        make_record("DOC-002"),
    ]

    result = build_version_audit(records)

    assert [
        row["Document ID"]
        for row in result
    ] == [
        "DOC-001",
        "DOC-002",
        "DOC-003",
    ]