from pathlib import Path

from docx import Document

from core.metadata import extract_metadata
from core.models import DocumentRecord


def scan_documents():
    """
    Scans all Word documents and returns a list of DocumentRecord objects.
    """

    project_root = Path(__file__).resolve().parents[2]

    docs_folder = project_root / "Documents"

    records = []

    print("\nScanning documents...\n")

    for file in docs_folder.glob("*.docx"):

        try:

            doc = Document(file)
            metadata = extract_metadata(file)

            headings = []

            for paragraph in doc.paragraphs:
                if paragraph.style.name.startswith("Heading"):
                    headings.append(paragraph.text.strip())

            record = DocumentRecord(
                file_path=file,
                file_name=file.name,
                document_id=metadata["Document ID"] or file.stem.split(" ")[0],
                title=metadata["Title"],
                document_type=file.stem.split("-")[0],
                version=metadata["Version"],
                status=metadata["Status"] or "OK",
                owner=metadata["Owner"],
                effective_date=metadata["Effective Date"],
                revision_date=metadata["Revision Date"],
                paragraph_count=len(doc.paragraphs),
                table_count=len(doc.tables),
                headings=headings,
            )

            records.append(record)

            print(f"✓ {record.file_name}")

        except Exception as ex:

            error_record = DocumentRecord(
                file_path=file,
                file_name=file.name,
            )

            error_record.errors.append(str(ex))

            records.append(error_record)

            print(f"✗ {file.name}")
            print(f"    {ex}")

    print(f"\nFinished.\n")
    print(f"{len(records)} documents processed.\n")

    return records