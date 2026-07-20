from pathlib import Path

from core.exporter import export_results
from core.scanner import scan_documents


def main():

    print("=" * 60)
    print("DD-BOS Engine v0.3.0")
    print("=" * 60)

    records = scan_documents()

    project_root = Path(__file__).resolve().parents[1]

    output_folder = project_root / "Output"
    output_folder.mkdir(exist_ok=True)

    output_file = output_folder / "Document Register.xlsx"

    export_results(records, output_file)

    print(f"Document Register written to:\n{output_file}")


if __name__ == "__main__":
    main()