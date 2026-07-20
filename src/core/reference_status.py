from dataclasses import dataclass


@dataclass
class ReferenceStatus:
    source_document: str
    referenced_document: str
    exists: bool
    message: str = ""