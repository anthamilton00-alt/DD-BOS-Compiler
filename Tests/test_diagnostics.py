from pathlib import Path

from core.diagnostics import build_diagnostics
from core.models import DocumentRecord


def make_record(
    document_id: str,
    errors: list[str] | None = None,
    missing_references: list[str] | None = None,
) -> DocumentRecord:
    return DocumentRecord(
        file_path=Path(f"{document_id}.docx"),
        file_name=f"{document_id}.docx",
        document_id=document_id,
        errors=errors or [],
        missing_references=missing_references or [],
    )


def test_ok_document():
    result = build_diagnostics(
        [
            make_record("DOC-001"),
        ]
    )

    assert result == [
        {
            "Document ID": "DOC-001",
            "Severity": "OK",
            "Error Count": 0,
            "Missing References": 0,
            "Message": "",
        }
    ]


def test_errors_set_error_severity():
    result = build_diagnostics(
        [
            make_record(
                "DOC-001",
                errors=["Invalid filename"],
            ),
        ]
    )

    assert result[0]["Severity"] == "Error"
    assert result[0]["Error Count"] == 1
    assert result[0]["Message"] == "Invalid filename"


def test_missing_references_set_warning_severity():
    result = build_diagnostics(
        [
            make_record(
                "DOC-001",
                missing_references=["DOC-999", "DOC-998"],
            ),
        ]
    )

    assert result[0]["Severity"] == "Warning"
    assert result[0]["Missing References"] == 2
    assert result[0]["Message"] == "2 Missing Reference(s)"


def test_errors_take_priority_over_warnings():
    result = build_diagnostics(
        [
            make_record(
                "DOC-001",
                errors=["Invalid metadata"],
                missing_references=["DOC-999"],
            ),
        ]
    )

    assert result[0]["Severity"] == "Error"
    assert result[0]["Message"] == (
        "Invalid metadata; 1 Missing Reference(s)"
    )


def test_results_are_sorted_by_document_id():
    result = build_diagnostics(
        [
            make_record("DOC-003"),
            make_record("DOC-001"),
            make_record("DOC-002"),
        ]
    )

    assert [
        row["Document ID"]
        for row in result
    ] == [
        "DOC-001",
        "DOC-002",
        "DOC-003",
    ]