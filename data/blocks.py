from dataclasses import dataclass

@dataclass
class Block:
    """Class for Block information."""
    breaking_time: int  # in ticks


class Stone(Block):

    def __init__(self):
        self.breaking_time_default = 150


class Air(Block):

    def __init__(self):
        self.breaking_time_default = 0


class Grass(Block):

    def __init__(self):
        self.breaking_time_default = 1


class Dirt(Block):

    def __init__(self):
        self.breaking_time_default = 0.75*20


class GrassBlock(Block):

    def __init__(self):
        self.breaking_time_default = 15


class Flower(Block):

    def __init__(self):
        self.breaking_time_default = 1


class Tulip(Flower):
    pass


class Log(Block):

    def __init__(self):
        self.breaking_time_default = 60


class Leaf(Block):

    def __init__(self):
        self.breaking_time_default = 1


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
