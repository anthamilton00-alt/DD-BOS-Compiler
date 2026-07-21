from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from core.reference_status import ReferenceStatus


@dataclass(frozen=True)
class ComplianceFinding:
    """
    A single compliance rule violation.
    """

    rule_id: str
    severity: str
    finding: str
    recommendation: str


@dataclass
class DocumentRecord:
    """
    Represents a parsed and validated DD-BOS document.
    """

    # ---------------------------------------------------------
    # File Information
    # ---------------------------------------------------------

    file_path: Path
    file_name: str

    # ---------------------------------------------------------
    # Metadata
    # ---------------------------------------------------------

    document_id: str = ""
    document_type: str = ""
    title: str = ""
    version: str = ""
    status: str = ""
    owner: str = ""
    effective_date: str = ""
    revision_date: str = ""

    # ---------------------------------------------------------
    # Parsed Content
    # ---------------------------------------------------------

    sections: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)

    # ---------------------------------------------------------
    # Reference Validation
    # ---------------------------------------------------------

    valid_references: List[str] = field(default_factory=list)
    missing_references: List[str] = field(default_factory=list)
    reference_statuses: List[ReferenceStatus] = field(default_factory=list)

    # ---------------------------------------------------------
    # Compliance
    # ---------------------------------------------------------

    compliance_findings: List[ComplianceFinding] = field(default_factory=list)

    # ---------------------------------------------------------
    # Statistics
    # ---------------------------------------------------------

    paragraph_count: int = 0
    table_count: int = 0

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    errors: List[str] = field(default_factory=list)

    @property
    def is_compliant(self) -> bool:
        """
        True when no compliance findings exist.
        """
        return len(self.compliance_findings) == 0

    @property
    def critical_findings(self) -> int:
        return sum(
            1
            for finding in self.compliance_findings
            if finding.severity == "Critical"
        )

    @property
    def high_findings(self) -> int:
        return sum(
            1
            for finding in self.compliance_findings
            if finding.severity == "High"
        )

    @property
    def medium_findings(self) -> int:
        return sum(
            1
            for finding in self.compliance_findings
            if finding.severity == "Medium"
        )

    @property
    def low_findings(self) -> int:
        return sum(
            1
            for finding in self.compliance_findings
            if finding.severity == "Low"
        )