from pathlib import Path

from core.duplicate_detector import find_duplicate_document_ids
from core.models import DocumentRecord


def make_record(
    document_id: str,
    file_name: str,
) -> DocumentRecord:
    return DocumentRecord(
        file_path=Path(file_name),
        file_name=file_name,
        document_id=document_id,
    )


def test_returns_empty_list_when_no_duplicates():
    records = [
        make_record("DOC-001", "DOC-001.docx"),
        make_record("DOC-002", "DOC-002.docx"),
    ]

    result = find_duplicate_document_ids(records)

    assert result == []


def test_detects_duplicate_document_ids():
    records = [
        make_record("DOC-001", "DOC-001 A.docx"),
        make_record("DOC-001", "DOC-001 B.docx"),
        make_record("DOC-002", "DOC-002.docx"),
    ]

    result = find_duplicate_document_ids(records)

    assert result == [
        {
            "Document ID": "DOC-001",
            "Occurrences": 2,
            "Files": "DOC-001 A.docx; DOC-001 B.docx",
        }
    ]


def test_sorts_duplicate_ids_and_file_names():
    records = [
        make_record("DOC-002", "Z.docx"),
        make_record("DOC-001", "B.docx"),
        make_record("DOC-002", "A.docx"),
        make_record("DOC-001", "A.docx"),
    ]

    result = find_duplicate_document_ids(records)

    assert result == [
        {
            "Document ID": "DOC-001",
            "Occurrences": 2,
            "Files": "A.docx; B.docx",
        },
        {
            "Document ID": "DOC-002",
            "Occurrences": 2,
            "Files": "A.docx; Z.docx",
        },
    ]


def test_counts_more_than_two_occurrences():
    records = [
        make_record("DOC-001", "A.docx"),
        make_record("DOC-001", "B.docx"),
        make_record("DOC-001", "C.docx"),
    ]

    result = find_duplicate_document_ids(records)

    assert result[0]["Occurrences"] == 3
    assert result[0]["Files"] == "A.docx; B.docx; C.docx"