"""Helper assert functions."""
from typing import Dict, Any


def are_equal(
    dict1: Dict[str, Any],
    dict2: Dict[str, Any],
    ignore_keys: Dict[str, Any]
):
    """To assert if two unsorted dictionaries are equal."""
    d1_filtered = {k: v for k, v in dict1.items() if k not in ignore_keys}
    d2_filtered = {k: v for k, v in dict2.items() if k not in ignore_keys}
    return d1_filtered == d2_filtered
