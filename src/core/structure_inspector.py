from pathlib import Path

import pandas as pd
from docx import Document


def inspect_document_structure():
    """
    Examines paragraph text, styles, and formatting in DD-BOS Word documents.

    Creates an Excel report that helps identify how section headings and
    document structure are represented when Word Heading styles are not used.
    """

    project_root = Path(__file__).resolve().parents[2]
    documents_folder = project_root / "Documents"
    output_folder = project_root / "Output"

    output_folder.mkdir(exist_ok=True)

    rows = []

    print("\nInspecting document structure...\n")

    files = sorted(documents_folder.glob("*.docx"))

    for file in files:
        try:
            document = Document(file)

            for paragraph_number, paragraph in enumerate(
                document.paragraphs,
                start=1,
            ):
                text = paragraph.text.strip()

                if not text:
                    continue

                runs = paragraph.runs

                bold_run_count = sum(
                    1 for run in runs if run.bold is True
                )

                italic_run_count = sum(
                    1 for run in runs if run.italic is True
                )

                font_sizes = sorted(
                    {
                        round(run.font.size.pt, 1)
                        for run in runs
                        if run.font.size is not None
                    }
                )

                all_bold = bool(runs) and all(
                    run.bold is True or not run.text.strip()
                    for run in runs
                )

                is_all_caps = (
                    any(character.isalpha() for character in text)
                    and text == text.upper()
                )

                likely_heading = (
                    len(text) <= 120
                    and (
                        all_bold
                        or is_all_caps
                        or text.endswith(":")
                    )
                )

                rows.append(
                    {
                        "File Name": file.name,
                        "Paragraph Number": paragraph_number,
                        "Text": text,
                        "Style": paragraph.style.name,
                        "Character Count": len(text),
                        "Run Count": len(runs),
                        "Bold Runs": bold_run_count,
                        "Italic Runs": italic_run_count,
                        "All Bold": all_bold,
                        "All Caps": is_all_caps,
                        "Ends With Colon": text.endswith(":"),
                        "Font Sizes": ", ".join(
                            str(size) for size in font_sizes
                        ),
                        "Likely Heading": likely_heading,
                    }
                )

            print(f"✓ {file.name}")

        except Exception as error:
            rows.append(
                {
                    "File Name": file.name,
                    "Paragraph Number": "",
                    "Text": "",
                    "Style": "",
                    "Character Count": "",
                    "Run Count": "",
                    "Bold Runs": "",
                    "Italic Runs": "",
                    "All Bold": "",
                    "All Caps": "",
                    "Ends With Colon": "",
                    "Font Sizes": "",
                    "Likely Heading": "",
                    "Error": str(error),
                }
            )

            print(f"✗ {file.name}")
            print(f"  {error}")

    report = pd.DataFrame(rows)

    output_file = output_folder / "Structure Inspection.xlsx"

    report.to_excel(output_file, index=False)

    print("\nInspection complete.")
    print(f"{len(files)} documents inspected.")
    print(f"\nReport written to:\n{output_file}")

    return output_file


if __name__ == "__main__":
    inspect_document_structure()