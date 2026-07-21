from pathlib import Path

from core.compiler import compile_order
from core.models import DocumentRecord


def make_record(
    document_id: str,
    references: list[str] | None = None,
) -> DocumentRecord:
    return DocumentRecord(
        file_path=Path(f"{document_id}.docx"),
        file_name=f"{document_id}.docx",
        document_id=document_id,
        document_type="Test",
        title=document_id,
        version="1.0",
        status="Active",
        owner="Test",
        effective_date="",
        revision_date="",
        sections=[],
        references=references or [],
        valid_references=[],
        missing_references=[],
        reference_statuses=[],
        paragraph_count=0,
        table_count=0,
        errors=[],
    )


def test_compile_order_without_dependencies():
    records = [
        make_record("DOC-003"),
        make_record("DOC-001"),
        make_record("DOC-002"),
    ]

    order, circular = compile_order(records)

    assert order == ["DOC-001", "DOC-002", "DOC-003"]
    assert circular == []


def test_dependency_compiles_before_dependent():
    records = [
        make_record("DOC-002", ["DOC-001"]),
        make_record("DOC-001"),
    ]

    order, circular = compile_order(records)

    assert order == ["DOC-001", "DOC-002"]
    assert circular == []


def test_multiple_dependency_levels():
    records = [
        make_record("DOC-003", ["DOC-002"]),
        make_record("DOC-002", ["DOC-001"]),
        make_record("DOC-001"),
    ]

    order, circular = compile_order(records)

    assert order == ["DOC-001", "DOC-002", "DOC-003"]
    assert circular == []


def test_external_references_are_ignored():
    records = [
        make_record("DOC-002", ["EXPECTED-001"]),
        make_record("DOC-001"),
    ]

    order, circular = compile_order(records)

    assert order == ["DOC-001", "DOC-002"]
    assert circular == []


def test_duplicate_references_do_not_create_false_cycle():
    records = [
        make_record("DOC-002", ["DOC-001", "DOC-001"]),
        make_record("DOC-001"),
    ]

    order, circular = compile_order(records)

    assert order == ["DOC-001", "DOC-002"]
    assert circular == []


def test_real_cycle_is_reported():
    records = [
        make_record("DOC-001", ["DOC-002"]),
        make_record("DOC-002", ["DOC-001"]),
        make_record("DOC-003"),
    ]

    order, circular = compile_order(records)

    assert order == ["DOC-003"]
    assert circular == ["DOC-001", "DOC-002"]