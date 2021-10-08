import logging
from random import randint

from perlin import Perlin
import numpy as np

from .block import Block
from .tree import Tree
from ...variables import (
    CHUNK_SIZE, TILE_SIZE, RENDER_DISTANCE, scroll, CHUNK_SIZE, MAX_HEIGHT, SEED
)

from . import generator

WATER_LEVEL = 63


LOG = logging.getLogger(__name__)
LOG.setLevel('DEBUG')

LOG.info('Using seed %d', SEED)
P_NOISE = Perlin(SEED)


class Chunk:

    def __init__(self, x, chunk_loaded=False, trees=False):
        LOG.debug("Creating chunk at %d", x)
        self.map = []
        self._tree_blocks = []
        self.placed_blocks = []
        self._x = x
        self.shape = (CHUNK_SIZE, MAX_HEIGHT)

        if trees:
            self._generate_trees()
        self._generate_terrain(chunk_loaded)

    def __iter__(self):
        return iter(self.map)

    def __getitem__(self, tup):
        if len(tup) == 1:
            return self.map(tup[0])
        elif len(tup) == 2:
            return self.map(tup[0] + tup[0]*self.shape[1])
        else:
            raise IndexError('Only 1 or 2D indexing available')

    def ground_level(self, x):
        """Get the first block that is not air"""
        for block in self.map[x*MAX_HEIGHT: (x + 1)*MAX_HEIGHT][::-1]:
            if block.type != 'air':
                return block.pos[1]//TILE_SIZE

    def _generate_trees(self):
        for target_y in range(self.shape[1]):
            for x_pos in range(self.shape[0]):
                target_x = self._x * CHUNK_SIZE + x_pos

                height = P_NOISE.one(target_x)

                if target_y == CHUNK_SIZE - 1 - height and randint(0, 6) == 0:
                    tree = Tree((target_x * TILE_SIZE, target_y * TILE_SIZE))
                    for tree_block in tree.blocks:
                        if tree_block.pos not in [i.pos for i in self._tree_blocks]:
                            self._tree_blocks.append(tree_block)

    def _generate_terrain(self, *args, **kwargs):
        x_dim, y_dim = CHUNK_SIZE, MAX_HEIGHT

        # grassland
        ground_level = generator.ground_level(0.0175, SEED, self._x*CHUNK_SIZE,
                                              x_dim, amp=40)

        coal = generator.blob(
            x_dim, y_dim, self._x*CHUNK_SIZE, SEED, self._x, n=5, max_height=127,
        )

        iron = generator.blob(
            x_dim, y_dim, self._x*CHUNK_SIZE, SEED, self._x, n=4, max_height=63,
        )
        
        diamond = generator.blob(
            x_dim, y_dim, self._x*CHUNK_SIZE, SEED, self._x, n=3, max_height=16,
        )
        gold = generator.blob(
            x_dim, y_dim, self._x*CHUNK_SIZE, SEED, self._x, n=3, max_height=32,
        )
        lapis = generator.blob(
            x_dim, y_dim, self._x*CHUNK_SIZE, SEED, self._x, n=3, max_height=32,
        )
        redstone = generator.blob(
            x_dim, y_dim, self._x*CHUNK_SIZE, SEED, self._x, n=3, max_height=16,
        )
        dirt = generator.blob(
            x_dim, y_dim, self._x*CHUNK_SIZE, SEED, self._x, n=20, max_height=128,
        )
        emerald = generator.blob(
            x_dim, y_dim, self._x*CHUNK_SIZE, SEED, self._x, n=1, max_height=32,
        )

        for x in range(x_dim):
            ground = ground_level[x]
            for y in range(y_dim)[::-1]:
                if y == MAX_HEIGHT - 1:
                    tile_type = 'bedrock'
                elif y < ground:
                    if y > WATER_LEVEL:
                        tile_type = 'water'
                    else:
                        tile_type = 'air'
                elif y == ground:
                    if y + 20 < WATER_LEVEL:
                        tile_type = 'grass_block_snow'
                    elif y - 2 < WATER_LEVEL:
                        tile_type = 'grass_block'
                    else:
                        tile_type = 'dirt'
                elif y < ground + 3:
                    tile_type = 'dirt'
                else:
                    flat_ind = y*x_dim + x
                    if flat_ind in iron:
                        tile_type = 'iron_ore'
                    elif flat_ind in coal:
                        tile_type = 'coal_ore'
                    elif flat_ind in diamond:
                        tile_type = 'diamond_ore'
                    elif flat_ind in gold:
                        tile_type = 'gold_ore'
                    elif flat_ind in lapis:
                        tile_type = 'lapis_ore'
                    elif flat_ind in redstone:
                        tile_type = 'redstone_ore'
                    elif flat_ind in dirt:
                        tile_type = 'dirt'
                    elif flat_ind in emerald:
                        tile_type = 'emerald_ore'
                    else:
                        tile_type = 'stone'

                target_x = self._x*CHUNK_SIZE + x
                block = Block((target_x*TILE_SIZE, y*TILE_SIZE), tile_type)
                self.map.append(block)

    def _generate_terrain_old(self, chunk_loaded):

        for target_y in range(MAX_HEIGHT):
            for x_pos in range(CHUNK_SIZE):

                block_added = False
                target_x = self._x * CHUNK_SIZE + x_pos

                height = P_NOISE.one(target_x)

                if target_y > CHUNK_SIZE + 3 - height:
                    tile_type = 'stone'
                elif target_y > CHUNK_SIZE - height:
                    tile_type = 'dirt'
                elif target_y == CHUNK_SIZE - height:
                    tile_type = 'grass_block'
                elif target_y == CHUNK_SIZE - 1 - height and randint(0, 6) == 0 and not chunk_loaded:
                    tile_type = 'tulip'
                elif target_y == CHUNK_SIZE - 1 - height and randint(0, 3) == 0 and not chunk_loaded:
                    tile_type = 'grass'
                else:
                    tile_type = 'air'

                for block in self.placed_blocks:
                    if block.coords == (target_x, target_y):
                        self.map.append(block)
                        block_added = True

                if not block_added:
                    if (target_x * TILE_SIZE, target_y * TILE_SIZE) in [i.pos for i in self._tree_blocks]:
                        if not chunk_loaded:
                            for tree_block in self._tree_blocks:
                                if tree_block.pos == (target_x * TILE_SIZE, target_y * TILE_SIZE):
                                    self.map.append(tree_block)
                                    self.placed_blocks.append(tree_block)
                    else:
                        block = Block((target_x * TILE_SIZE, target_y * TILE_SIZE), tile_type)
                        self.map.append(block)
                        if tile_type in ['tulip', 'grass']:
                            self.placed_blocks.append(Block((target_x * TILE_SIZE, target_y * TILE_SIZE), tile_type))


# if __name__ == '__main__':
#     chunk = Chunk()
