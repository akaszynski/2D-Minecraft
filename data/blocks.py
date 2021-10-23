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

class Furnace(Block):

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

class Fire(Block):

    def __init__(self):
        self.hardness = 0.00001
        self.harvest = []
        self.placeable = True

class Cake(Block):

    def __init__(self):
        self.hardness = 0.00001
        self.harvest = []
        self.placeable = True

class LargeCake(Block):

    def __init__(self):
        self.hardness = 0.00001
        self.harvest = []
        self.placeable = True

class LargeCakeInside(Block):

    def __init__(self):
        self.hardness = 0.00001
        self.harvest = []
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


class Painting(Block):

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
        
class Glass(Block):

    def __init__(self):
        self.hardness = 0.03
        self.harvest = []
        self.placeable = True

class Glass_Pane(Block):

    def __init__(self):
        self.hardness = 0.03
        self.harvest = []
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
        self.placeable = True


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

class OakPlanks(Block):

    def __init__(self):
        self.hardness = 2
        self.harvest = [None, 'axe']
        self.placeable = True

class DarkOakSign(Block):

    def __init__(self):
        self.hardness = 2
        self.harvest = [None, 'axe']
        self.placeable = True

# items
#########################################################
class Item(Block):

    def __init__(self):
        self.hardness = 0
        self.harvest = []
        self.placeable = False

class Apple(Item):
    pass

class Bow(Item):
    pass

class Diamond(Item):
    pass

class Coal(Item):
    pass

class Emerald(Item):
    pass

class Book(Item):
    pass

class Redstone(Item):
    pass

class LapusLazuli(Item):
    pass

#########################################################


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


class Oak_leaf(Block):

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
    'oak_leaf': Oak_leaf(),
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
    'glass': Glass(),
    'glass_pane': Glass_Pane(),
    'dark_oak_sign': DarkOakSign(),
    'oak_planks': OakPlanks(),
    'paintingp': Painting(),
    'fire': Fire(),
    'cake': Cake(),
    'large_cake': LargeCake(),
    'large_cake_inside': LargeCakeInside(),
    'furnace': Furnace(),
##################################################
    'apple': Apple(),
    'bow': Bow(),
    'coal': Coal(),
    'diamond': Diamond(),
    'emerald': Emerald(),
    'book': Book(),
    'redstone': Redstone(),
    'lapis_lazuli': LapusLazuli(),
    
}
