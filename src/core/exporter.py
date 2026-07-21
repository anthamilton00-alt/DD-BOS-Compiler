from pathlib import Path
from typing import Any

import pandas as pd
from openpyxl.styles import Font


def _sanitize_excel_value(value: Any) -> Any:
    """
    Prevent document text from being written as an Excel formula.
    """

    if isinstance(value, str) and value.startswith("="):
        return f"'{value}"

    return value


def _sanitize_rows(rows: list[dict]) -> list[dict]:
    """
    Sanitize every value before exporting it to Excel.
    """

    return [
        {
            key: _sanitize_excel_value(value)
            for key, value in row.items()
        }
        for row in rows
    ]


def _auto_format_sheet(worksheet) -> None:
    """
    Apply standard formatting to an exported worksheet.
    """

    worksheet.freeze_panes = "A2"
    worksheet.auto_filter.ref = worksheet.dimensions

    for cell in worksheet[1]:
        cell.font = Font(bold=True)

    for column_cells in worksheet.columns:
        width = max(
            len(str(cell.value)) if cell.value is not None else 0
            for cell in column_cells
        )

        worksheet.column_dimensions[
            column_cells[0].column_letter
        ].width = min(width + 2, 60)


def export_results(
    records,
    output_path: Path,
    dependency_graph: dict[str, set[str]] | None = None,
    compile_order: list[str] | None = None,
    circular_dependencies: list[str] | None = None,
    cross_reference_index: dict[str, list[str]] | None = None,
    health_results: list[dict] | None = None,
    diagnostics: list[dict] | None = None,
    dashboard: list[dict] | None = None,
    duplicate_documents: list[dict] | None = None,
    orphan_documents: list[dict] | None = None,
    reference_coverage: list[dict] | None = None,
    risk_scores: list[dict] | None = None,
    change_impact: list[dict] | None = None,
    version_audit: list[dict] | None = None,
    owner_summary: list[dict] | None = None,
    compliance_report: list[dict] | None = None,
    compliance_dashboard: list[dict] | None = None,
) -> None:
    """
    Export all DD-BOS compilation results to an Excel workbook.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    dependency_graph = dependency_graph or {}
    compile_order = compile_order or []
    circular_dependencies = circular_dependencies or []
    cross_reference_index = cross_reference_index or {}
    health_results = health_results or []
    diagnostics = diagnostics or []
    dashboard = dashboard or []
    duplicate_documents = duplicate_documents or []
    orphan_documents = orphan_documents or []
    reference_coverage = reference_coverage or []
    risk_scores = risk_scores or []
    change_impact = change_impact or []
    version_audit = version_audit or []
    owner_summary = owner_summary or []
    compliance_report = compliance_report or []
    compliance_dashboard = compliance_dashboard or []

    document_rows = []
    section_rows = []
    reference_rows = []
    impact_rows = []
    compile_rows = []
    cross_reference_rows = []

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
                "Valid References": len(record.valid_references),
                "Missing References": len(record.missing_references),
                "Compliance Status": (
                    "Compliant"
                    if record.is_compliant
                    else "Non-Compliant"
                ),
                "Compliance Findings": len(
                    record.compliance_findings
                ),
                "Critical Findings": record.critical_findings,
                "High Findings": record.high_findings,
                "Medium Findings": record.medium_findings,
                "Low Findings": record.low_findings,
                "Errors": "; ".join(record.errors),
            }
        )

        for index, section in enumerate(record.sections, start=1):
            section_rows.append(
                {
                    "Document ID": record.document_id,
                    "File Name": record.file_name,
                    "Section Order": index,
                    "Section": section,
                }
            )

        for status in record.reference_statuses:
            reference_rows.append(
                {
                    "Source Document": status.source_document,
                    "Referenced Document": status.referenced_document,
                    "Exists": status.exists,
                    "Status": status.message,
                }
            )

    for changed_document in sorted(dependency_graph):
        for affected_document in sorted(
            dependency_graph[changed_document]
        ):
            impact_rows.append(
                {
                    "Changed Document": changed_document,
                    "Affected Document": affected_document,
                }
            )

    for position, document_id in enumerate(
        compile_order,
        start=1,
    ):
        compile_rows.append(
            {
                "Compile Order": position,
                "Document ID": document_id,
                "Status": "Ready",
            }
        )

    for document_id in circular_dependencies:
        compile_rows.append(
            {
                "Compile Order": "",
                "Document ID": document_id,
                "Status": "Circular Dependency",
            }
        )

    for referenced_document, sources in sorted(
        cross_reference_index.items()
    ):
        for source_document in sorted(sources):
            cross_reference_rows.append(
                {
                    "Referenced Document": referenced_document,
                    "Referenced By": source_document,
                }
            )

    sheets = {
        "Compliance Dashboard": compliance_dashboard,
        "Compliance Report": compliance_report,
        "Dashboard": dashboard,
        "Documents": document_rows,
        "Sections": section_rows,
        "References": reference_rows,
        "Impact Analysis": impact_rows,
        "Compile Order": compile_rows,
        "Cross References": cross_reference_rows,
        "Document Health": health_results,
        "Diagnostics": diagnostics,
        "Duplicate Documents": duplicate_documents,
        "Orphan Documents": orphan_documents,
        "Reference Coverage": reference_coverage,
        "Risk Scores": risk_scores,
        "Change Impact": change_impact,
        "Version Audit": version_audit,
        "Owner Summary": owner_summary,
    }

    with pd.ExcelWriter(
        output_path,
        engine="openpyxl",
    ) as writer:
        for sheet_name, rows in sheets.items():
            sanitized_rows = _sanitize_rows(rows)

            pd.DataFrame(sanitized_rows).to_excel(
                writer,
                sheet_name=sheet_name,
                index=False,
            )

            _auto_format_sheet(
                writer.sheets[sheet_name]
            )