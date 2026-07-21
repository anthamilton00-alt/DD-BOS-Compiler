import argparse
from collections.abc import Sequence

from core.change_impact import build_change_impact
from core.compiler import compile_order
from core.config import load_config
from core.coverage import build_reference_coverage
from core.cross_reference import build_cross_reference_index
from core.dashboard import build_dashboard
from core.dependency_graph import build_dependency_graph
from core.diagnostics import build_diagnostics
from core.document_health import evaluate_document_health
from core.duplicate_detector import find_duplicate_document_ids
from core.exporter import export_results
from core.orphan_detector import find_orphan_documents
from core.owner_summary import build_owner_summary
from core.risk_score import build_risk_scores
from core.scanner import scan_documents
from core.validator import validate_references
from core.version_audit import build_version_audit


def count_health_issues(issues) -> int:
    """
    Convert a health issue value into a consistent issue count.
    """

    if not issues:
        return 0

    if isinstance(issues, (list, tuple, set)):
        return len(issues)

    if isinstance(issues, str):
        return len(
            [
                issue
                for issue in issues.split(";")
                if issue.strip()
            ]
        )

    return 1


def build_parser() -> argparse.ArgumentParser:
    """
    Build the DD-BOS command-line interface.
    """

    config = load_config()

    parser = argparse.ArgumentParser(
        prog="dd-bos",
        description=(
            "Compile and validate the Digitally Defined "
            "Business Operating System document library."
        ),
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"DD-BOS Engine v{config.engine_version}",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        metavar="COMMAND",
    )

    subparsers.add_parser(
        "compile",
        help="Compile the document library and export the Excel register.",
    )

    subparsers.add_parser(
        "validate",
        help="Scan and validate the document library without exporting.",
    )

    return parser


def run_validation() -> int:
    """
    Scan and validate the document library without creating an export.
    """

    config = load_config()

    print("=" * 60)
    print(f"DD-BOS Engine v{config.engine_version}")
    print("=" * 60)
    print()

    records = scan_documents()

    if not records:
        print("No documents were found.")
        return 1

    validate_references(records)

    diagnostics = build_diagnostics(records)

    error_count = sum(
        len(record.errors)
        for record in records
    )

    print()
    print("=" * 60)
    print("Validation Summary")
    print("=" * 60)
    print(f"Documents              : {len(records)}")
    print(f"Diagnostics            : {len(diagnostics)}")
    print(f"Processing Errors      : {error_count}")

    if error_count:
        print()
        print("Validation completed with errors.")
        return 1

    print()
    print("Validation completed successfully.")
    return 0


def run_compile() -> int:
    """
    Compile the DD-BOS library and export the document register.
    """

    config = load_config()

    print("=" * 60)
    print(f"DD-BOS Engine v{config.engine_version}")
    print("=" * 60)
    print()

    records = scan_documents()

    if not records:
        print("No documents were found.")
        return 1

    validate_references(records)

    dependency_graph = build_dependency_graph(records)
    cross_reference_index = build_cross_reference_index(records)

    health_results = evaluate_document_health(records)
    diagnostics = build_diagnostics(records)

    order, circular = compile_order(records)

    dashboard = build_dashboard(
        records=records,
        health_results=health_results,
        diagnostics=diagnostics,
        cross_reference_index=cross_reference_index,
        circular_dependencies=circular,
    )

    duplicate_documents = find_duplicate_document_ids(records)

    orphan_documents = find_orphan_documents(
        records,
        cross_reference_index,
    )

    reference_coverage = build_reference_coverage(
        records,
        cross_reference_index,
    )

    health_issue_counts = {
        row["Document ID"]: count_health_issues(
            row.get("Issues")
        )
        for row in health_results
    }

    inbound_reference_counts = {
        row["Document ID"]: row["Inbound References"]
        for row in reference_coverage
    }

    risk_scores = build_risk_scores(
        records,
        health_issue_counts,
        inbound_reference_counts,
    )

    change_impact = build_change_impact(
        records,
        cross_reference_index,
    )

    version_audit = build_version_audit(records)
    owner_summary = build_owner_summary(records)

    config.output_folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    export_results(
        records=records,
        output_path=config.output_file,
        dependency_graph=dependency_graph,
        compile_order=order,
        circular_dependencies=circular,
        cross_reference_index=cross_reference_index,
        health_results=health_results,
        diagnostics=diagnostics,
        dashboard=dashboard,
        duplicate_documents=duplicate_documents,
        orphan_documents=orphan_documents,
        reference_coverage=reference_coverage,
        risk_scores=risk_scores,
        change_impact=change_impact,
        version_audit=version_audit,
        owner_summary=owner_summary,
    )

    processing_error_count = sum(
        len(record.errors)
        for record in records
    )

    print()
    print("=" * 60)
    print("Compilation Summary")
    print("=" * 60)
    print(f"Engine Version         : {config.engine_version}")
    print(f"Documents              : {len(records)}")
    print(
        f"Cross References       : "
        f"{sum(len(v) for v in cross_reference_index.values())}"
    )
    print(f"Dashboard Metrics      : {len(dashboard)}")
    print(f"Health Records         : {len(health_results)}")
    print(f"Diagnostics            : {len(diagnostics)}")
    print(f"Circular Dependencies  : {len(circular)}")
    print(f"Duplicate Documents    : {len(duplicate_documents)}")
    print(f"Orphan Documents       : {len(orphan_documents)}")
    print(f"Reference Coverage     : {len(reference_coverage)}")
    print(f"Risk Scores            : {len(risk_scores)}")
    print(f"Change Impact Records  : {len(change_impact)}")
    print(f"Version Audit Records  : {len(version_audit)}")
    print(f"Owner Summary Records  : {len(owner_summary)}")
    print(f"Processing Errors      : {processing_error_count}")
    print()
    print(f"Document Register written to:\n{config.output_file}")

    return 1 if processing_error_count else 0


def main(argv: Sequence[str] | None = None) -> int:
    """
    Run the requested DD-BOS command.
    """

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "validate":
        return run_validation()

    return run_compile()


if __name__ == "__main__":
    raise SystemExit(main())