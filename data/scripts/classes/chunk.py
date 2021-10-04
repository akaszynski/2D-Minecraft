from random import randint
import perlin

from .block import Block
from .tree import Tree
from ...variables import CHUNK_SIZE, TILE_SIZE, RENDER_DISTANCE, scroll, CHUNK_SIZE, MAX_HEIGHT

p = perlin.Perlin(randint(0, 99999))

import logging

LOG = logging.getLogger(__name__)
LOG.setLevel('DEBUG')


class Chunk:

    def __init__(self, x, chunk_loaded):
        LOG.debug("Creating chunk at %d", x)
        self.map = []
        self._tree_blocks = []
        self.placed_blocks = []
        self._x = x

        self._generate_trees()
        self._generate_terrain(chunk_loaded)

    def __iter__(self):
        return iter(self.map)

    def _generate_trees(self):
        for target_y in range(MAX_HEIGHT):
            for x_pos in range(CHUNK_SIZE):

                target_x = self._x * CHUNK_SIZE + x_pos

                height = p.one(target_x)

                if target_y == CHUNK_SIZE - 1 - height and randint(0, 6) == 0:
                    tree = Tree((target_x * TILE_SIZE, target_y * TILE_SIZE))
                    for tree_block in tree.blocks:
                        if tree_block.pos not in [i.pos for i in self._tree_blocks]:
                            self._tree_blocks.append(tree_block)

    def _generate_terrain(self, chunk_loaded):

        for target_y in range(MAX_HEIGHT):
            for x_pos in range(CHUNK_SIZE):

                block_added = False
                target_x = self._x * CHUNK_SIZE + x_pos

                height = p.one(target_x)

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
