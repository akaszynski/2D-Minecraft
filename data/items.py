from dataclasses import dataclass


@dataclass
class Item:
    """Class for Block information."""
    hardness: float
    harvest: list
    