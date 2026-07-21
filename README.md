# DD-BOS Compiler

The DD-BOS Compiler scans the Digitally Defined Business Operating System document library and generates a governance workbook.

## Features

- Document scanning
- Metadata extraction
- Reference validation
- Dependency graph
- Compile order
- Circular dependency detection
- Cross-reference analysis
- Document health scoring
- Diagnostics
- Duplicate detection
- Orphan detection
- Reference coverage
- Risk scoring
- Change impact analysis
- Version audit
- Owner summary

## Requirements

- Python 3.11+
- Microsoft Word (.docx) documents

## Installation

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

## Compile

```bash
python src/main.py
```

or

```bash
python src/main.py compile
```

## Validate Only

```bash
python src/main.py validate
```

## Help

```bash
python src/main.py --help
```

## Output

The compiler generates:

```
Output/
    Document Register.xlsx
```

## Test Suite

```bash
pytest -q
```

## Current Status

- Engine Version: 1.0.0
- Test Status: 57 passing
- Excel Workbook: 16 worksheets