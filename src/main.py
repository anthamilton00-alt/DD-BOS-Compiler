from pathlib import Path

from core.dependency_graph import build_dependency_graph
from core.exporter import export_results
from core.scanner import scan_documents
from core.validator import validate_references


def main():

    print("=" * 60)
    print("DD-BOS Engine v0.4.0")
    print("=" * 60)

    records = scan_documents()

    validate_references(records)

    dependency_graph = build_dependency_graph(records)

    project_root = Path(__file__).resolve().parents[1]

    output_folder = project_root / "Output"
    output_folder.mkdir(exist_ok=True)

    output_file = output_folder / "Document Register.xlsx"

    export_results(
        records,
        output_file,
        dependency_graph=dependency_graph,
    )

    print(f"Document Register written to:\n{output_file}")


if __name__ == "__main__":
    main()