from threading import Thread
import logging
import perlin
from random import randint

from .block import Block
from data.scripts.classes.player import Player
from .chunk import Chunk
from ...variables import CHUNK_SIZE, TILE_SIZE, RENDER_DISTANCE, scroll, CHUNK_SIZE
from ...variables import RENDER_DISTANCE as RDIST
from ..core_functions import distance

p = perlin.Perlin(randint(0, 99999))

LOG = logging.getLogger(__name__)
LOG.setLevel('DEBUG')

# blocks with no colisions
NON_COL_BLOCKS = ['air', 'grass', 'tulip', 'water', 'torch', 'lava', 'dark_oak_sign', 'paintingp', 'fire', 'cake', 'crafting_table', 'furnace']


def threaded(func):
    """Decorator to call a function using a thread"""

    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


class Terrain:

    def __init__(self, initialize=True, threaded=True, lighting=False):
        self.tile_rects = []
        self.placed_blocks = []
        self.chunks = {}  # all chunks
        self.active_chunks = {}
        self._future_chunks = {}
        self._threaded = threaded
        self._lighting_changed = True
        self._lighting = lighting
        self._player_position = None

        # initialze world
        if initialize and threaded:
            self._initialize()

    def _initialize(self, base_chunk=0):
        # start threads for any chunks beyond render distance
        future_chunks = range(base_chunk - 2*RDIST, base_chunk + 2*RDIST + 1)
        for xx in future_chunks:
            if xx not in self.chunks and xx not in self._future_chunks:
                self._future_chunks[xx] = self.generate_chunk_background(xx)

        for thread in self._future_chunks.values():
            thread.join()

    def remove_block(self, block_pos):
        for block in self:
            if block.pos == block_pos:
                block.type = 'air'
                self.placed_blocks.append(block)
                self._lighting_changed = True

    def __iter__(self):
        for chunk in self.active_chunks.values():
            for block in chunk:
                yield block

    def add_block(self, block_pos, block_type):
        for block in self:
            if block.pos == block_pos:
                if block_type not in ['tulip', 'grass']:
                    if block.type in ['air', 'water', 'lava']:
                        block.type = block_type
                        self.placed_blocks.append(block)
                        self._lighting_changed = True
                        return True
                else:
                    for block2 in self:
                        if block2.pos == (block_pos[0], block_pos[1] + TILE_SIZE):
                            if block2.type != 'air':
                                block.type = block_type
                                self.placed_blocks.append(block)
                                return True
                            else:
                                return False

    def generate_hitbox(self, player):
        rects = [block.rect for block in self if block.type not in NON_COL_BLOCKS]
        self.tile_rects = rects

    def draw(self, display):
        for chunk in list(self.active_chunks.values()):
            chunk.draw(display)

    def generate_chunk(self, x):
        """Generate chunk"""
        if x in self._future_chunks:
            self._future_chunks[x].join()
        else:
            self.chunks[x] = Chunk(x, self, False)

        self.active_chunks[x] = self.chunks[x]

    @threaded
    def generate_chunk_background(self, x):
        """Generate chunk in the background"""
        LOG.debug('Generating chunk %d in background thread', x)
        self.chunks[x] = Chunk(x, self, False)

    def ground_level(self, x):
        """Return the ground level at a position"""
        return self.chunks[0].ground_level(0)

    def _update_chunks(self, base_chunk):
        """Update the chunks that are active"""
        target_chunks = range(base_chunk - RDIST, base_chunk + RDIST + 1)
        for xx in target_chunks:
            if xx not in self.active_chunks:
                if xx not in self.chunks:
                    self.generate_chunk(xx)
                else:
                    LOG.debug('Activating chunk %d', xx)
                    self.active_chunks[xx] = self.chunks[xx]

        # remove any chunks no longer active
        extra_chunks = set(self.active_chunks) - set(target_chunks)
        for chunk in extra_chunks:
            del self.active_chunks[chunk]

        # start threads for any chunks beyond render distance
        if self._threaded:
            future_chunks = range(base_chunk - 2*RDIST, base_chunk + 2*RDIST + 1)
            for xx in future_chunks:
                if xx in target_chunks:
                    continue

                # create thread
                if xx not in self.chunks and xx not in self._future_chunks:
                    self._future_chunks[xx] = self.generate_chunk_background(xx)

    # def _update_visibility(self, player):
    #     for block in self:
    #         if abs(block.coords[0] - player.coords[0]) < 2:
    #             ydist = block.coords[1] - player.coords[1]
    #             if ydist < 3 and ydist > -2:
    #                 block.visited = True

    def _update_lighting(self, force=False):
        if self._lighting_changed or force:
            for block in self:
                if block.type == 'torch':
                    block.illumination = 14
                    block.light = 14
                elif block.type == 'glowstone':
                    block.illumination = 15
                elif block.type == 'lava':
                    block.illumination = 15
                elif block.type == 'fire':
                    block.illumination = 15
                else:
                    block.illumination = 0
                    block.light = 0

            LOG.debug('Updating lighting')
            for chunk in list(self.chunks.values()):
                chunk.update_sky_lighting(14)

            for block in self:
                if block.illumination:
                    block.flood_light()

            self._lighting_changed = False

    @property
    def player_position(self):
        return self._player_position

    @player_position.setter
    def player_position(self, value):
        self._player_position = value

    def update(self, player):
        self.generate_hitbox(player)

        if player.chunk_changed:
            LOG.debug('Chunk changed')
            
            self._update_chunks(player.current_chunk)
            self._lighting_changed = True

        if self._lighting:
            self._update_lighting()
        else:
            for block in self:
                block.light = 15

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
