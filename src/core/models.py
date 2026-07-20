from dataclasses import dataclass, field
from pathlib import Path
from typing import List


@dataclass
class DocumentRecord:
    """
    Represents one DD-BOS document inside the engine.
    Every document loaded by the scanner becomes one of these.
    """

    file_path: Path
    file_name: str

    document_id: str = ""
    title: str = ""
    document_type: str = ""
    version: str = ""
    status: str = ""
    owner: str = ""

    effective_date: str = ""
    revision_date: str = ""

    paragraph_count: int = 0
    table_count: int = 0

    headings: List[str] = field(default_factory=list)

    references: List[str] = field(default_factory=list)

    errors: List[str] = field(default_factory=list)