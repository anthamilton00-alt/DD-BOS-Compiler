from collections import defaultdict

from core.models import DocumentRecord


def build_compile_graph(records: list[DocumentRecord]) -> dict[str, list[str]]:
    """
    Build a directed dependency graph.

    Result:

        FP-0001 -> [ROOM-001, ROOM-002, DD-012]
    """

    graph = defaultdict(list)

    for record in records:
        graph[record.document_id] = sorted(
            set(reference.upper() for reference in record.references)
        )

    return dict(graph)