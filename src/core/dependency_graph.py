from collections import defaultdict

from core.models import DocumentRecord


def build_dependency_graph(records: list[DocumentRecord]) -> dict[str, set[str]]:
    """
    Build a reverse dependency graph.

    Key   = document that is referenced.
    Value = documents that reference it.

    Example:

        ROOM-001:
            ASM-202
            FP-0001

    Self-references are ignored because they do not represent a
    dependency and they inflate circular dependency, impact, and
    inbound reference calculations.
    """

    graph: dict[str, set[str]] = defaultdict(set)

    for record in records:
        source = record.document_id.upper()

        for reference in record.references:
            target = reference.upper()

            # Ignore blank references
            if not target:
                continue

            # Ignore self-references
            if target == source:
                continue

            graph[target].add(source)

    return dict(graph)