from collections import Counter
from typing import Iterable

from core.models import ComplianceFinding, DocumentRecord
from core.registry import VALID_OWNERS, VALID_STATUSES


RULES = {
    "DD-COMP-001": {
        "severity": "Critical",
        "finding": "Missing Document ID",
        "recommendation": "Assign a valid DD-BOS document ID.",
    },
    "DD-COMP-002": {
        "severity": "High",
        "finding": "Missing Owner",
        "recommendation": "Assign a valid owner from the DD-BOS registry.",
    },
    "DD-COMP-003": {
        "severity": "High",
        "finding": "Missing Version",
        "recommendation": "Populate the document version metadata field.",
    },
    "DD-COMP-004": {
        "severity": "High",
        "finding": "Missing Status",
        "recommendation": "Assign a valid document status from the DD-BOS registry.",
    },
    "DD-COMP-005": {
        "severity": "Medium",
        "finding": "Missing Effective Date",
        "recommendation": "Populate the effective date metadata field.",
    },
    "DD-COMP-006": {
        "severity": "Low",
        "finding": "Missing Revision Date",
        "recommendation": "Populate the revision date metadata field when applicable.",
    },
    "DD-COMP-007": {
        "severity": "Critical",
        "finding": "Invalid Status",
        "recommendation": "Replace the status with a valid value from the DD-BOS registry.",
    },
    "DD-COMP-008": {
        "severity": "High",
        "finding": "Invalid Owner",
        "recommendation": "Replace the owner with a valid value from the DD-BOS registry.",
    },
    "DD-COMP-009": {
        "severity": "Critical",
        "finding": "Duplicate Document ID",
        "recommendation": "Assign a unique document ID and resolve the duplicate record.",
    },
    "DD-COMP-010": {
        "severity": "High",
        "finding": "Orphan Document",
        "recommendation": "Add a valid relationship to the document or confirm that it is intentionally standalone.",
    },
    "DD-COMP-011": {
        "severity": "Critical",
        "finding": "Circular Dependency",
        "recommendation": "Remove or redesign references that create the circular dependency.",
    },
    "DD-COMP-012": {
        "severity": "Critical",
        "finding": "Processing Error",
        "recommendation": "Correct the document or compiler error before release.",
    },
    "DD-COMP-013": {
        "severity": "Critical",
        "finding": "Missing Title",
        "recommendation": "Assign a clear and controlled document title.",
    },
}


def create_finding(rule_id: str) -> ComplianceFinding:
    """
    Create a compliance finding from the controlled rule registry.
    """

    rule = RULES[rule_id]

    return ComplianceFinding(
        rule_id=rule_id,
        severity=rule["severity"],
        finding=rule["finding"],
        recommendation=rule["recommendation"],
    )


def normalize_ids(values: Iterable[str] | None) -> set[str]:
    """
    Normalize document ID collections for reliable comparison.
    """

    if not values:
        return set()

    return {
        str(value).strip().upper()
        for value in values
        if str(value).strip()
    }


def evaluate_compliance(
    records: list[DocumentRecord],
    orphan_document_ids: Iterable[str] | None = None,
    circular_document_ids: Iterable[str] | None = None,
) -> list[DocumentRecord]:
    """
    Evaluate all documents against DD-BOS compliance rules.

    Existing findings are replaced each time this function runs.
    """

    orphan_ids = normalize_ids(orphan_document_ids)
    circular_ids = normalize_ids(circular_document_ids)

    document_id_counts = Counter(
        record.document_id.strip().upper()
        for record in records
        if record.document_id.strip()
    )

    valid_owners = {
        owner.strip().casefold()
        for owner in VALID_OWNERS
    }

    valid_statuses = {
        status.strip().upper()
        for status in VALID_STATUSES
    }

    for record in records:
        record.compliance_findings.clear()

        document_id = record.document_id.strip()
        normalized_document_id = document_id.upper()

        owner = record.owner.strip()
        status = record.status.strip()

        if not document_id:
            record.compliance_findings.append(
                create_finding("DD-COMP-001")
            )

        if not record.title.strip():
            record.compliance_findings.append(
                create_finding("DD-COMP-013")
            )

        if not owner:
            record.compliance_findings.append(
                create_finding("DD-COMP-002")
            )
        elif owner.casefold() not in valid_owners:
            record.compliance_findings.append(
                create_finding("DD-COMP-008")
            )

        if not record.version.strip():
            record.compliance_findings.append(
                create_finding("DD-COMP-003")
            )

        if not status:
            record.compliance_findings.append(
                create_finding("DD-COMP-004")
            )
        elif status.upper() not in valid_statuses:
            record.compliance_findings.append(
                create_finding("DD-COMP-007")
            )

        if not record.effective_date.strip():
            record.compliance_findings.append(
                create_finding("DD-COMP-005")
            )

        if not record.revision_date.strip():
            record.compliance_findings.append(
                create_finding("DD-COMP-006")
            )

        if (
            normalized_document_id
            and document_id_counts[normalized_document_id] > 1
        ):
            record.compliance_findings.append(
                create_finding("DD-COMP-009")
            )

        if normalized_document_id in orphan_ids:
            record.compliance_findings.append(
                create_finding("DD-COMP-010")
            )

        if normalized_document_id in circular_ids:
            record.compliance_findings.append(
                create_finding("DD-COMP-011")
            )

        if record.errors:
            record.compliance_findings.append(
                create_finding("DD-COMP-012")
            )

    return records


def build_compliance_report(
    records: list[DocumentRecord],
) -> list[dict]:
    """
    Flatten document findings into export-ready report rows.
    """

    rows = []

    for record in records:
        for finding in record.compliance_findings:
            rows.append(
                {
                    "Document ID": record.document_id,
                    "File Name": record.file_name,
                    "Title": record.title,
                    "Owner": record.owner,
                    "Rule ID": finding.rule_id,
                    "Severity": finding.severity,
                    "Finding": finding.finding,
                    "Recommendation": finding.recommendation,
                }
            )

    return rows


def build_compliance_dashboard(
    records: list[DocumentRecord],
) -> list[dict]:
    """
    Build executive compliance metrics and release-gate status.
    """

    total_documents = len(records)

    compliant_documents = sum(
        1
        for record in records
        if record.is_compliant
    )

    non_compliant_documents = (
        total_documents - compliant_documents
    )

    critical_findings = sum(
        record.critical_findings
        for record in records
    )

    high_findings = sum(
        record.high_findings
        for record in records
    )

    medium_findings = sum(
        record.medium_findings
        for record in records
    )

    low_findings = sum(
        record.low_findings
        for record in records
    )

    compliance_percentage = (
        round(
            compliant_documents / total_documents * 100,
            2,
        )
        if total_documents
        else 100.0
    )

    if critical_findings:
        release_status = "FAIL"
    elif high_findings or medium_findings or low_findings:
        release_status = "PASS WITH WARNINGS"
    else:
        release_status = "PASS"

    return [
        {
            "Metric": "Total Documents",
            "Value": total_documents,
        },
        {
            "Metric": "Compliant Documents",
            "Value": compliant_documents,
        },
        {
            "Metric": "Non-Compliant Documents",
            "Value": non_compliant_documents,
        },
        {
            "Metric": "Critical Findings",
            "Value": critical_findings,
        },
        {
            "Metric": "High Findings",
            "Value": high_findings,
        },
        {
            "Metric": "Medium Findings",
            "Value": medium_findings,
        },
        {
            "Metric": "Low Findings",
            "Value": low_findings,
        },
        {
            "Metric": "Overall Compliance",
            "Value": f"{compliance_percentage:.2f}%",
        },
        {
            "Metric": "Release Status",
            "Value": release_status,
        },
    ]