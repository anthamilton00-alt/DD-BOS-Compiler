from collections import deque

from core.models import DocumentRecord


def compile_order(records: list[DocumentRecord]) -> tuple[list[str], list[str]]:
    """
    Return documents in dependency-safe compile order.

    Documents referenced by another document compile first.
    References to documents outside the current record set are ignored.
    """

    document_ids = {record.document_id for record in records}

    adjacency: dict[str, set[str]] = {
        document_id: set()
        for document_id in document_ids
    }

    indegree: dict[str, int] = {
        document_id: 0
        for document_id in document_ids
    }

    for record in records:
        internal_references = {
            reference.upper()
            for reference in record.references
            if reference.upper() in document_ids
        }

        for dependency in internal_references:
            adjacency[dependency].add(record.document_id)
            indegree[record.document_id] += 1

    queue = deque(
        sorted(
            document_id
            for document_id, degree in indegree.items()
            if degree == 0
        )
    )

    order: list[str] = []

    while queue:
        document_id = queue.popleft()
        order.append(document_id)

        for dependent in sorted(adjacency[document_id]):
            indegree[dependent] -= 1

            if indegree[dependent] == 0:
                queue.append(dependent)

    circular = sorted(
        document_id
        for document_id, degree in indegree.items()
        if degree > 0
    )

    return order, circular