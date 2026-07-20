from pathlib import Path

import pandas as pd

from core.scanner import scan_documents


def main():

    print("=" * 60)
    print("DD-BOS Engine v0.2.0")
    print("=" * 60)

    records = scan_documents()

    project_root = Path(__file__).resolve().parents[1]

    output_folder = project_root / "Output"
    output_folder.mkdir(exist_ok=True)

    rows = []

    for record in records:

        rows.append(
            {
                "File Name": record.file_name,
                "Document ID": record.document_id,
                "Document Type": record.document_type,
                "Title": record.title,
                "Version": record.version,
                "Status": record.status,
                "Owner": record.owner,
                "Paragraphs": record.paragraph_count,
                "Tables": record.table_count,
                "Headings": len(record.headings),
                "Errors": "; ".join(record.errors),
            }
        )

    df = pd.DataFrame(rows)

    output_file = output_folder / "Document Register.xlsx"

    df.to_excel(output_file, index=False)

    print(f"Document Register written to:\n{output_file}")


if __name__ == "__main__":
    main()