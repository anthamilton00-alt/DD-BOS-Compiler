from typing import List

from core.models import DocumentRecord
from core.reference_status import ReferenceStatus
from core.reference_rules import classify_reference


def validate_references(records: List[DocumentRecord]) -> None:
    """
    Validate every cross-document reference against the scanned document set.

    Populates:
        - valid_references
        - missing_references
        - reference_statuses
        - errors
    """

    known_document_ids = {
        record.document_id.upper()
        for record in records
        if record.document_id
    }

    for record in records:

        record.valid_references.clear()
        record.missing_references.clear()
        record.reference_statuses.clear()
        record.errors.clear()

        for reference in record.references:

            reference = reference.upper()

            exists, status = classify_reference(
                reference,
                known_document_ids,
            )

            if exists:
                record.valid_references.append(reference)
            else:
                record.missing_references.append(reference)

            record.reference_statuses.append(
                ReferenceStatus(
                    source_document=record.document_id,
                    referenced_document=reference,
                    exists=exists,
                    message=status,
                )
            )

            if status == "Invalid":
                record.errors.append(
                    f"Invalid document reference: {reference}"
                )

        expected_count = sum(
            1
            for item in record.reference_statuses
            if item.message == "Expected"
        )

        if expected_count:
            record.errors.append(
                f"{expected_count} expected document(s) not yet present"
            )