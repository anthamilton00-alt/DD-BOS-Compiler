from pathlib import Path

from core.models import DocumentRecord
from core.orphan_detector import find_orphan_documents


def make_record(
    document_id: str,
    title: str = "",
    owner: str = "",
) -> DocumentRecord:
    return DocumentRecord(
        file_path=Path(f"{document_id}.docx"),
        file_name=f"{document_id}.docx",
        document_id=document_id,
        title=title,
        owner=owner,
    )


def test_returns_empty_list_when_all_documents_are_referenced():
    records = [
        make_record("DOC-001"),
        make_record("DOC-002"),
    ]

    cross_reference_index = {
        "DOC-001": ["DOC-002"],
        "DOC-002": ["DOC-001"],
    }

    result = find_orphan_documents(
        records,
        cross_reference_index,
    )

    assert result == []


def test_detects_orphan_documents():
    records = [
        make_record(
            "DOC-001",
            title="Referenced Document",
            owner="Operations",
        ),
        make_record(
            "DOC-002",
            title="Orphan Document",
            owner="Finance",
        ),
    ]

    cross_reference_index = {
        "DOC-001": ["DOC-002"],
    }

    result = find_orphan_documents(
        records,
        cross_reference_index,
    )

    assert result == [
        {
            "Document ID": "DOC-002",
            "Title": "Orphan Document",
            "Owner": "Finance",
        }
    ]


def test_returns_all_documents_when_index_is_empty():
    records = [
        make_record("DOC-002"),
        make_record("DOC-001"),
    ]

    result = find_orphan_documents(
        records,
        {},
    )

    assert result == [
        {
            "Document ID": "DOC-001",
            "Title": "",
            "Owner": "",
        },
        {
            "Document ID": "DOC-002",
            "Title": "",
            "Owner": "",
        },
    ]


def test_results_are_sorted_by_document_id():
    records = [
        make_record("DOC-003"),
        make_record("DOC-001"),
        make_record("DOC-002"),
    ]

    result = find_orphan_documents(
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