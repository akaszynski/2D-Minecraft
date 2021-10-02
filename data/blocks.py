"""
The base time in seconds is the block's hardness multiplied by 1.5 if
the player can harvest the block with the current tool, or 5 if the
player cannot.
"""

from dataclasses import dataclass

@dataclass
class Block:
    """Class for Block information."""
    hardness: float


class Stone(Block):

    def __init__(self):
        self.hardness = 1.5


class Air(Block):

    def __init__(self):
        self.hardness = 0


class Grass(Block):

    def __init__(self):
        self.hardness = 0


class Dirt(Block):

    def __init__(self):
        self.hardness = 0.5


class GrassBlock(Block):

    def __init__(self):
        self.hardness = 0.5


class Flower(Block):

    def __init__(self):
        self.hardness = 0


class Tulip(Flower):
    pass


class Log(Block):

    def __init__(self):
        self.hardness = 2


class Leaf(Block):

    def __init__(self):
        self.hardness = 0.2


blocks = {
    'stone': Stone(),
    'air': Air(),
    'grass': Grass(),
    'dirt': Dirt(),
    'grass_block': GrassBlock(),
    'tulip': Tulip(),
    'oak_log': Log(),
    'leaf': Leaf(),

}
