from pathlib import Path

from core.cross_reference import build_cross_reference_index
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


def test_builds_reverse_reference_index():
    records = [
        make_record("DOC-001"),
        make_record("DOC-002", ["DOC-001"]),
        make_record("DOC-003", ["DOC-001"]),
    ]

    result = build_cross_reference_index(records)

    assert result == {
        "DOC-001": ["DOC-002", "DOC-003"],
    }


def test_ignores_external_references():
    records = [
        make_record("DOC-001", ["EXPECTED-001"]),
        make_record("DOC-002"),
    ]

    result = build_cross_reference_index(records)

    assert result == {}


def test_removes_duplicate_referrers():
    records = [
        make_record("DOC-001"),
        make_record("DOC-002", ["DOC-001", "DOC-001"]),
    ]

    result = build_cross_reference_index(records)

    assert result == {
        "DOC-001": ["DOC-002"],
    }


def test_normalizes_reference_case():
    records = [
        make_record("DOC-001"),
        make_record("DOC-002", ["doc-001"]),
    ]

    result = build_cross_reference_index(records)

    assert result == {
        "DOC-001": ["DOC-002"],
    }


def test_returns_sorted_documents_and_referrers():
    records = [
        make_record("DOC-003", ["DOC-002", "DOC-001"]),
        make_record("DOC-002"),
        make_record("DOC-001"),
    ]

    result = build_cross_reference_index(records)

    assert list(result) == ["DOC-001", "DOC-002"]
    assert result["DOC-001"] == ["DOC-003"]
    assert result["DOC-002"] == ["DOC-003"]