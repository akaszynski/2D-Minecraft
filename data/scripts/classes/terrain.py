import logging
import perlin
from random import randint

from .block import Block
from .chunk import Chunk
from ...variables import CHUNK_SIZE, TILE_SIZE, RENDER_DISTANCE, scroll, CHUNK_SIZE

p = perlin.Perlin(randint(0, 99999))

LOG = logging.getLogger(__name__)
LOG.setLevel('DEBUG')

# blocks with no colisions
NON_COL_BLOCKS = ['air', 'grass', 'tulip', 'oak_log', 'leaf']



class Terrain:

    def __init__(self):
        self.map = []
        self.tile_rects = []
        self.placed_blocks = []
        self.chunks = {}
        self.active_chunks = set()

    # @property
    # def map(self):
    #     for chunk in self.chunks.items:
    #         yield chunk.map

    def unload_chunk(self, chunk_pos):
        for block in self.map:
            if block.chunk == chunk_pos:
                self.map.remove(block)

    def remove_block(self, block_pos):
        for i, block in enumerate(self.map):
            if block.pos == block_pos:
                self.map[i].type = 'air'
                self.placed_blocks.append(self.map[i])

    def add_block(self, block_pos, block_type):
        for i, block in enumerate(self.map):
            if block.pos == block_pos:
                if block_type not in ['tulip', 'grass']:
                    if block.type == 'air':
                        self.map[i].type = block_type
                        self.placed_blocks.append(self.map[i])
                        return True
                else:
                    for block2 in self.map:
                        if block2.pos == (block_pos[0], block_pos[1] + TILE_SIZE):
                            if block2.type != 'air':
                                self.map[i].type = block_type
                                self.placed_blocks.append(self.map[i])
                                return True
                            else:
                                return False

    def generate_hitbox(self, player):
        rects = [block.rect for block in self.map if block.type not in NON_COL_BLOCKS]
        self.tile_rects = rects

    def draw(self, display):
        # LOG.debug("map size %d", len(self.map))
        for block in self.map:
            display.blit(block.img, block.get_scrolled_pos(scroll))

    def generate_chunk(self, x):
        """Generate chunk"""
        # if x not in self.loaded_chunks:
        chunk_loaded = False
        chunk = Chunk(x, chunk_loaded)
        self.map.extend(chunk.map)
        self.chunks[x] = chunk

    def load_chunk(self, x):
        self.map.extend(self.chunks[x].map)

    def update(self, player):
        self.generate_hitbox(player)

        target_chunks = set()
        for x in range(RENDER_DISTANCE):
            target_x = x + player.current_chunk[0] - RENDER_DISTANCE//2
            target_chunks.add(target_x)
            if target_x not in self.active_chunks:
                if target_x not in self.chunks:
                    self.generate_chunk(target_x)
                else:
                    self.load_chunk(target_x)
            self.active_chunks.add(target_x)

        # remove any chunks no longer active
        extra_chunks = self.active_chunks - target_chunks
        for chunk in extra_chunks:
            self.unload_chunk(chunk)
        self.active_chunks = target_chunks

        # # remove placed blocks if air below
        # for i, block in enumerate(self.map):
        #     if block.type in ['tulip', 'grass']:
        #         for block2 in self.map:
        #             if block2.pos == (block.pos[0], block.pos[1] + TILE_SIZE):
        #                 if block2.type == 'air':
        #                     try:
        #                         self.placed_blocks.remove(self.map[i])
        #                     except ValueError:
        #                         pass
        #                     self.map[i].type = 'air'

        # print(self.map[0].coords)

        # compute lighting
        # for i, block in enumerate(self.map):
        #     if not block.visible:
        #         breakpoint()

    # def block_below(self, block):
    #     """Return the block below the given block if loaded"""
    #     if block.coords[1] == 0:
    #         # chunk_below(self, 0):
            

    # def chunk_below(self, 0):
