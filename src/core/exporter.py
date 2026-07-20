from pathlib import Path

import pandas as pd


def export_results(records, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    document_rows = []
    section_rows = []
    reference_rows = []

    for record in records:
        document_rows.append(
            {
                "Document ID": record.document_id,
                "Document Type": record.document_type,
                "Title": record.title,
                "Version": record.version,
                "Status": record.status,
                "Owner": record.owner,
                "Effective Date": record.effective_date,
                "Revision Date": record.revision_date,
                "File Name": record.file_name,
                "Paragraph Count": record.paragraph_count,
                "Table Count": record.table_count,
                "Section Count": len(record.sections),
                "Reference Count": len(record.references),
                "Errors": "; ".join(record.errors),
            }
        )

        for position, section in enumerate(record.sections, start=1):
            section_rows.append(
                {
                    "Document ID": record.document_id,
                    "File Name": record.file_name,
                    "Section Order": position,
                    "Section": section,
                }
            )

        for reference in record.references:
            reference_rows.append(
                {
                    "Source Document ID": record.document_id,
                    "Source File": record.file_name,
                    "Referenced Document ID": reference,
                }
            )

    documents_df = pd.DataFrame(document_rows)
    sections_df = pd.DataFrame(
        section_rows,
        columns=["Document ID", "File Name", "Section Order", "Section"],
    )
    references_df = pd.DataFrame(
        reference_rows,
        columns=[
            "Source Document ID",
            "Source File",
            "Referenced Document ID",
        ],
    )

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        documents_df.to_excel(writer, sheet_name="Documents", index=False)
        sections_df.to_excel(writer, sheet_name="Sections", index=False)
        references_df.to_excel(writer, sheet_name="References", index=False)

        for worksheet in writer.book.worksheets:
            worksheet.freeze_panes = "A2"
            worksheet.auto_filter.ref = worksheet.dimensions

            for column_cells in worksheet.columns:
                width = max(
                    len(str(cell.value)) if cell.value is not None else 0
                    for cell in column_cells
                )
                worksheet.column_dimensions[column_cells[0].column_letter].width = min(
                    width + 2,
                    60,
                )