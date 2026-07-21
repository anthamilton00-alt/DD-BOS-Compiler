from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CompilerConfig:
    """
    Runtime configuration for the DD-BOS Compiler.
    """

    project_root: Path
    input_folder: Path
    output_folder: Path
    output_file: Path
    engine_version: str


def load_config() -> CompilerConfig:
    """
    Build the default compiler configuration from the project location.
    """

    project_root = Path(__file__).resolve().parents[2]
    input_folder = project_root / "Documents"
    output_folder = project_root / "Output"
    output_file = output_folder / "Document Register.xlsx"

    return CompilerConfig(
        project_root=project_root,
        input_folder=input_folder,
        output_folder=output_folder,
        output_file=output_file,
        engine_version="1.0.0",
    )