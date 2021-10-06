from threading import Thread
import logging
import perlin
from random import randint

from .block import Block
from .chunk import Chunk
from ...variables import CHUNK_SIZE, TILE_SIZE, RENDER_DISTANCE, scroll, CHUNK_SIZE
from ...variables import RENDER_DISTANCE as RDIST

p = perlin.Perlin(randint(0, 99999))

LOG = logging.getLogger(__name__)
LOG.setLevel('DEBUG')

# blocks with no colisions
NON_COL_BLOCKS = ['air', 'grass', 'tulip', 'oak_log', 'leaf', 'water']


def threaded(func):
    """Decorator to call a function using a thread"""

    def wrapper(*args, **kwargs):
        thread = Thread(target=func, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper


class Terrain:

    def __init__(self, initialize=True, threaded=True):
        self.tile_rects = []
        self.placed_blocks = []
        self.chunks = {}  # all chunks
        self.active_chunks = {}
        self._future_chunks = {}
        self._threaded = threaded

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

    def __iter__(self):
        for chunk in self.active_chunks.values():
            for block in chunk:
                yield block

    def add_block(self, block_pos, block_type):
        for block in self:
            if block.pos == block_pos:
                if block_type not in ['tulip', 'grass']:
                    if block.type in ['air', 'water']:
                        block.type = block_type
                        self.placed_blocks.append(block)
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
        for block in self:
            display.blit(block.img, block.get_scrolled_pos(scroll))

    def generate_chunk(self, x):
        """Generate chunk"""
        if x in self._future_chunks:
            self._future_chunks[x].join()
        else:
            chunk_loaded = False
            self.chunks[x] = Chunk(x, chunk_loaded)

        self.active_chunks[x] = self.chunks[x]

    @threaded
    def generate_chunk_background(self, x):
        """Generate chunk in the background"""
        LOG.debug('Generating chunk %d in background thread', x)
        chunk_loaded = False
        self.chunks[x] = Chunk(x, chunk_loaded)

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

    def update(self, player):
        self.generate_hitbox(player)

        if player.chunk_changed:
            self._update_chunks(player.current_chunk)

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
