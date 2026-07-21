from pathlib import Path

from core.document_health import evaluate_document_health
from core.models import DocumentRecord


def make_record(
    document_id: str,
    title: str = "Test Document",
    version: str = "1.0",
    owner: str = "Test Owner",
    errors: list[str] | None = None,
    missing_references: list[str] | None = None,
) -> DocumentRecord:
    return DocumentRecord(
        file_path=Path(f"{document_id}.docx"),
        file_name=f"{document_id}.docx",
        document_id=document_id,
        title=title,
        version=version,
        owner=owner,
        errors=errors or [],
        missing_references=missing_references or [],
    )


def test_healthy_document_scores_100():
    records = [
        make_record("DOC-001"),
    ]

    result = evaluate_document_health(records)

    assert result == [
        {
            "Document ID": "DOC-001",
            "Health Score": 100,
            "Issues": "",
        }
    ]


def test_missing_metadata_reduces_score():
    records = [
        make_record(
            "DOC-001",
            title="",
            version="",
            owner="",
        ),
    ]

    result = evaluate_document_health(records)

    assert result[0]["Health Score"] == 70
    assert result[0]["Issues"] == (
        "Missing Title; Missing Version; Missing Owner"
    )


def test_errors_reduce_score():
    records = [
        make_record(
            "DOC-001",
            errors=[
                "Invalid filename",
                "Missing required section",
            ],
        ),
    ]

    result = evaluate_document_health(records)

    assert result[0]["Health Score"] == 90
    assert result[0]["Issues"] == (
        "Invalid filename; Missing required section"
    )


def test_missing_references_reduce_score():
    records = [
        make_record(
            "DOC-001",
            missing_references=[
                "DOC-999",
                "DOC-998",
            ],
        ),
    ]

    result = evaluate_document_health(records)

    assert result[0]["Health Score"] == 90
    assert result[0]["Issues"] == "2 Missing Reference(s)"


def test_score_never_goes_below_zero():
    records = [
        make_record(
            "DOC-001",
            title="",
            version="",
            owner="",
            errors=[f"Error {number}" for number in range(20)],
            missing_references=[f"DOC-{number}" for number in range(20)],
        ),
    ]

    result = evaluate_document_health(records)

    assert result[0]["Health Score"] == 0


def test_results_are_sorted_by_document_id():
    records = [
        make_record("DOC-003"),
        make_record("DOC-001"),
        make_record("DOC-002"),
    ]

    result = evaluate_document_health(records)

    assert [
        row["Document ID"]
        for row in result
    ] == [
        "DOC-001",
        "DOC-002",
        "DOC-003",
    ]