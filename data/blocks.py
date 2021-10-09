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
    harvest: list


class Bedrock(Block):

    def __init__(self):
        self.hardness = -1
        self.harvest = [None]


class Stone(Block):

    def __init__(self):
        self.hardness = 1.5
        self.harvest = ['pickaxe']


class Ore(Block):
    
    def __init__(self):
        self.hardness = 3
        self.harvest = ['pickaxe']


class CoalOre(Ore):
    pass


class IronOre(Ore):
    pass


class DiamondOre(Ore):
    pass


class EmeraldOre(Ore):
    pass


class LapisOre(Ore):
    pass


class RedstoneOre(Ore):
    pass


class GoldOre(Ore):
    pass


class Air(Block):

    def __init__(self):
        self.hardness = 0
        self.harvest = [None]


class Water(Block):

    def __init__(self):
        self.hardness = 0
        self.harvest = [None]


class Grass(Block):

    def __init__(self):
        self.hardness = 0
        self.harvest = [None]


class Dirt(Block):

    def __init__(self):
        self.hardness = 0.5
        self.harvest = [None, 'shovel']


class GrassBlock(Block):

    def __init__(self):
        self.hardness = 0.5
        self.harvest = [None, 'shovel']

class SnowGrassBlock(Block):

    def __init__(self):
        self.hardness = 0.5
        self.harvest = [None, 'shovel']


class Flower(Block):

    def __init__(self):
        self.hardness = 0
        self.harvest = [None]


class Tulip(Flower):
    pass


class Log(Block):

    def __init__(self):
        self.hardness = 2
        self.harvest = [None, 'axe']
        
class Sand(Block):

    def __init__(self):
        self.hardness = 0.5
        self.harvest = [None, 'shovel']


class Leaf(Block):

    def __init__(self):
        self.hardness = 0.2
        self.harvest = [None, 'hoe']


blocks = {
    'stone': Stone(),
    'air': Air(),
    'grass': Grass(),
    'dirt': Dirt(),
    'grass_block': GrassBlock(),
    'tulip': Tulip(),
    'oak_log': Log(),
    'leaf': Leaf(),
    'bedrock': Bedrock(),
    'coal_ore': CoalOre(),
    'iron_ore': IronOre(),
    'water': Water(),
    'sand': Sand(),
    'diamond_ore': DiamondOre(),
    'gold_ore': GoldOre(),
    'lapis_ore': LapisOre(),
    'redstone_ore': RedstoneOre(),
    'emerald_ore': EmeraldOre(),
    'grass_block_snow': SnowGrassBlock(),
}
