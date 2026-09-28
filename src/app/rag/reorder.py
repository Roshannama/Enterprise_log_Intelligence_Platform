from __future__ import annotations


def reorder_context(results: list[dict]) -> list[dict]:
    """
    Reorder retrieved chunks to distribute highly
    relevant information across the final context.

    Input:
        [1, 2, 3, 4, 5, 6]

    Output:
        [1, 3, 5, 6, 4, 2]
    """
    if len(results) <= 2:
        return results
    ordered = list(results)
    left = ordered[::2]
    right = ordered[1::2]
    reordered = left + list(reversed(right))
    return reordered
