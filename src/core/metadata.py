from docx import Document

METADATA_FIELDS = [
    "Document ID",
    "Title",
    "Version",
    "Status",
    "Owner",
    "Effective Date",
    "Revision Date",
]


def extract_metadata(doc_path):
    """
    Reads a Word document and extracts simple metadata lines.
    Expected format:
        Document ID: ASM-202
        Version: 1.0
        Status: Approved
    """

    doc = Document(doc_path)

    metadata = {field: "" for field in METADATA_FIELDS}

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()

        for field in METADATA_FIELDS:
            prefix = f"{field}:"

            if text.startswith(prefix):
                metadata[field] = text[len(prefix):].strip()

    return metadata