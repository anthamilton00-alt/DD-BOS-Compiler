from collections import defaultdict

from core.models import DocumentRecord


def build_dependency_graph(records: list[DocumentRecord]) -> dict[str, set[str]]:
    """
    Returns a reverse dependency graph.

    Example:

        ROOM-001:
            ASM-202
            FP-0001
    """

    graph = defaultdict(set)

    for record in records:
        for reference in record.references:
            graph[reference.upper()].add(record.document_id)

    return dict(graph)