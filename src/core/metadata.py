from pathlib import Path
import re

from docx import Document


METADATA_FIELDS = {
    "Document ID": "",
    "Title": "",
    "Version": "",
    "Status": "",
    "Owner": "",
    "Effective Date": "",
    "Revision Date": "",
}

LABEL_MAP = {
    "DOCUMENT ID": "Document ID",
    "ASSEMBLY ID": "Document ID",
    "ROOM ID": "Document ID",
    "FLOOR PLAN ID": "Document ID",

    "DOCUMENT NAME": "Title",
    "ASSEMBLY NAME": "Title",
    "ROOM NAME": "Title",
    "FLOOR PLAN NAME": "Title",

    "VERSION": "Version",
    "STATUS": "Status",
    "DOCUMENT OWNER": "Owner",
    "OWNER": "Owner",
    "EFFECTIVE DATE": "Effective Date",
    "REVISION DATE": "Revision Date",
}

DOCUMENT_ID_PATTERN = re.compile(
    r"\b(?:ASM|DD|FP|ROOM)-\d+\b",
    re.IGNORECASE,
)

VERSION_PATTERN = re.compile(r"^\d+(?:\.\d+)*$")

VALID_STATUSES = {
    "DRAFT",
    "ACTIVE",
    "APPROVED",
    "FROZEN",
    "ARCHIVED",
    "RETIRED",
}

INVALID_VALUES = {
    "",
    "DATE",
    "DATE:",
    "DATE APPROVED",
    "DATE APPROVED:",
    "BUILDER FLOOR PLAN NUMBER",
    "BUILDER FLOOR PLAN NUMBER:",
    "DOCUMENT ID",
    "DOCUMENT ID:",
    "ASSEMBLY ID",
    "ASSEMBLY ID:",
    "ROOM ID",
    "ROOM ID:",
    "FLOOR PLAN ID",
    "FLOOR PLAN ID:",
    "DOCUMENT NAME",
    "DOCUMENT NAME:",
    "ASSEMBLY NAME",
    "ASSEMBLY NAME:",
    "ROOM NAME",
    "ROOM NAME:",
    "FLOOR PLAN NAME",
    "FLOOR PLAN NAME:",
    "VERSION",
    "VERSION:",
    "STATUS",
    "STATUS:",
    "OWNER",
    "OWNER:",
    "DOCUMENT OWNER",
    "DOCUMENT OWNER:",
    "EFFECTIVE DATE",
    "EFFECTIVE DATE:",
    "REVISION DATE",
    "REVISION DATE:",
}


def clean_value(value: str) -> str:
    value = value.strip()

    if value.upper() in INVALID_VALUES:
        return ""

    if value and all(character in {"_", "-", " "} for character in value):
        return ""

    return value


def extract_filename_metadata(doc_path):
    stem = Path(doc_path).stem.strip()

    document_id = ""
    title = ""

    id_match = DOCUMENT_ID_PATTERN.search(stem)

    if id_match:
        document_id = id_match.group(0).upper()

    title_parts = re.split(r"\s+[—–]\s+", stem, maxsplit=1)

    if len(title_parts) == 2:
        title = title_parts[1].strip()

    return document_id, title


def extract_metadata(doc_path):
    """
    Extract DD-BOS metadata from a Word document.

    The standardized filename is authoritative for Document ID and Title.
    Document content supplies Version, Status, Owner, and date fields.
    """

    doc = Document(doc_path)
    metadata = METADATA_FIELDS.copy()

    filename_id, filename_title = extract_filename_metadata(doc_path)

    metadata["Document ID"] = filename_id
    metadata["Title"] = filename_title

    paragraphs = [
        paragraph.text.strip()
        for paragraph in doc.paragraphs
        if paragraph.text.strip()
    ]

    for index, text in enumerate(paragraphs[:-1]):
        label = text.rstrip(":").strip().upper()

        if label not in LABEL_MAP:
            continue

        field = LABEL_MAP[label]
        value = clean_value(paragraphs[index + 1])

        if not value:
            continue

        if field == "Document ID":
            if not metadata["Document ID"]:
                id_match = DOCUMENT_ID_PATTERN.search(value)

                if id_match:
                    metadata["Document ID"] = id_match.group(0).upper()

        elif field == "Title":
            if not metadata["Title"]:
                metadata["Title"] = value

        elif field == "Version":
            if VERSION_PATTERN.fullmatch(value):
                metadata["Version"] = value

        elif field == "Status":
            normalized_status = value.upper()

            if normalized_status in VALID_STATUSES:
                metadata["Status"] = normalized_status

        else:
            metadata[field] = value

    return metadata