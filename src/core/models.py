from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class DocumentRecord:
    """
    Represents a parsed DD-BOS document.
    """

    # File Information
    file_path: Path
    file_name: str

    # Metadata
    document_id: str = ""
    document_type: str = ""
    title: str = ""
    version: str = ""
    status: str = ""
    owner: str = ""
    effective_date: str = ""
    revision_date: str = ""

    # Parsed Content
    sections: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)

    # Statistics
    paragraph_count: int = 0
    table_count: int = 0

    # Validation
    errors: List[str] = field(default_factory=list)