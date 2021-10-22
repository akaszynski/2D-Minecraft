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
    placeable: bool


class Bedrock(Block):

    def __init__(self):
        self.hardness = -1
        self.harvest = [None]
        self.placeable = True


class Stone(Block):

    def __init__(self):
        self.hardness = 1.5
        self.harvest = ['pickaxe']
        self.placeable = True

class CobbleStone(Block):

    def __init__(self):
        self.hardness = 1.5
        self.harvest = ['pickaxe']
        self.placeable = True

class GlowStone(Block):

    def __init__(self):
        self.hardness = 1.5
        self.harvest = ['pickaxe']
        self.placeable = True


class Ore(Block):
    
    def __init__(self):
        self.hardness = 3
        self.harvest = ['pickaxe']
        self.placeable = True


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
        self.placeable = True




class Water(Block):

    def __init__(self):
        self.hardness = 0
        self.harvest = [None]
        self.placeable = True

class Lava(Block):

    def __init__(self):
        self.hardness = 0
        self.harvest = [None]
        self.placeable = True


class Grass(Block):

    def __init__(self):
        self.hardness = 0.0001
        self.harvest = [None, 'axe', 'pickaxe', 'shovel', 'hoe']
        self.placeable = True

class SlimeBlock(Block):

    def __init__(self):
        self.hardness = 0.0001
        self.harvest = [None, 'axe', 'pickaxe', 'shovel', 'hoe']
        self.placeable = True

class Scaffolding(Block):

    def __init__(self):
        self.hardness = 0.0001
        self.harvest = [None, 'axe', 'pickaxe', 'shovel', 'hoe']
        self.placeable = True

class Dirt(Block):

    def __init__(self):
        self.hardness = 0.5
        self.harvest = [None, 'shovel']
        self.placeable = True


class GrassBlock(Block):

    def __init__(self):
        self.hardness = 0.5
        self.harvest = [None, 'shovel']
        self.placeable = True

class SnowGrassBlock(Block):

    def __init__(self):
        self.hardness = 0.5
        self.harvest = [None, 'shovel']


class Flower(Block):

    def __init__(self):
        self.hardness = 0.0001
        self.harvest = [None, 'axe', 'pickaxe', 'shovel', 'hoe']
        self.placeable = True

class Torch(Block):

    def __init__(self):
        self.hardness = 0.0001
        self.harvest = [None, 'axe', 'pickaxe', 'shovel', 'hoe']
        self.placeable = True


class Tulip(Flower):
    pass


class Log(Block):

    def __init__(self):
        self.hardness = 2
        self.harvest = [None, 'axe']
        self.placeable = True

class CraftingTable(Block):

    def __init__(self):
        self.hardness = 2
        self.harvest = [None, 'axe']
        self.placeable = True

class BookShelf(Block):

    def __init__(self):
        self.hardness = 1.5
        self.harvest = [None, 'axe']
        self.placeable = True
        
class TNT(Block):

    def __init__(self):
        self.hardness = 0.0001
        self.harvest = [None, 'axe', 'pickaxe', 'shovel', 'hoe']
        self.placeable = True

class Sand(Block):

    def __init__(self):
        self.hardness = 0.5
        self.harvest = [None, 'shovel']
        self.placeable = True


class Leaf(Block):

    def __init__(self):
        self.hardness = 0.2
        self.harvest = [None, 'hoe']
        self.placeable = True


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
    'bookshelf': BookShelf(),
    'torch': Torch(),
    'tnt': TNT(),
    'glowstone': GlowStone(),
    'crafting_table': CraftingTable(),
    'lava': Lava(),
    'cobblestone': CobbleStone(),
    'slime_block': SlimeBlock(),
    'scaffolding': Scaffolding(),
}
