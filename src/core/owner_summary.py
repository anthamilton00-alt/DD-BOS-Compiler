from collections import defaultdict

from core.models import DocumentRecord


def build_owner_summary(
    records: list[DocumentRecord],
) -> list[dict]:
    """
    Summarize document ownership.

    Returns one row per owner showing how many
    documents they are responsible for.
    """

    counts = defaultdict(int)

    for record in records:
        owner = (record.owner or "").strip()

        if not owner:
            owner = "Unassigned"

        counts[owner] += 1

    return [
        {
            "Owner": owner,
            "Document Count": counts[owner],
        }
        for owner in sorted(counts)
    ]