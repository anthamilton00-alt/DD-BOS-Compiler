from collections import deque

from core.models import DocumentRecord


def _tarjan_scc(
    graph: dict[str, set[str]],
) -> list[list[str]]:
    """
    Find strongly connected components using Tarjan's algorithm.
    """

    index = 0
    indices: dict[str, int] = {}
    lowlinks: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    components: list[list[str]] = []

    def strongconnect(node: str) -> None:
        nonlocal index

        indices[node] = index
        lowlinks[node] = index
        index += 1

        stack.append(node)
        on_stack.add(node)

        for neighbor in graph[node]:
            if neighbor not in indices:
                strongconnect(neighbor)
                lowlinks[node] = min(
                    lowlinks[node],
                    lowlinks[neighbor],
                )
            elif neighbor in on_stack:
                lowlinks[node] = min(
                    lowlinks[node],
                    indices[neighbor],
                )

        if lowlinks[node] == indices[node]:
            component: list[str] = []

            while True:
                member = stack.pop()
                on_stack.remove(member)
                component.append(member)

                if member == node:
                    break

            components.append(component)

    for node in sorted(graph):
        if node not in indices:
            strongconnect(node)

    return components


def compile_order(
    records: list[DocumentRecord],
) -> tuple[list[str], list[str]]:
    """
    Return dependency-safe compile order.

    Circular dependencies are reported only for documents that are
    members of actual dependency cycles.
    """

    document_ids = {
        record.document_id.upper()
        for record in records
    }

    graph: dict[str, set[str]] = {
        document_id: set()
        for document_id in document_ids
    }

    indegree = {
        document_id: 0
        for document_id in document_ids
    }

    for record in records:

        source = record.document_id.upper()

        dependencies = {
            reference.upper()
            for reference in record.references
            if (
                reference.upper() in document_ids
                and reference.upper() != source
            )
        }

        for dependency in dependencies:

            if source not in graph[dependency]:
                graph[dependency].add(source)
                indegree[source] += 1

    queue = deque(
        sorted(
            node
            for node, degree in indegree.items()
            if degree == 0
        )
    )

    order: list[str] = []

    while queue:

        node = queue.popleft()
        order.append(node)

        for dependent in sorted(graph[node]):

            indegree[dependent] -= 1

            if indegree[dependent] == 0:
                queue.append(dependent)

    components = _tarjan_scc(graph)

    circular: list[str] = []

    for component in components:

        if len(component) > 1:
            circular.extend(component)
            continue

        node = component[0]

        if node in graph[node]:
            circular.append(node)

    circular = sorted(set(circular))

    return order, circular