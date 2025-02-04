import pygame
import os

from ...variables import TILE_SIZE, MAX_HEIGHT, CHUNK_SIZE

pygame.init()
pygame.display.set_mode()


BLOCK_TEXTURE_SZ = (TILE_SIZE, TILE_SIZE)
imgs_dir = 'data/imgs/blocks'

block_imgs = {}
shaders = {}
for img in os.listdir(imgs_dir):
    loaded_img = pygame.image.load(imgs_dir + '/' + img).convert_alpha()
    loaded_img = pygame.transform.scale(loaded_img, (TILE_SIZE, TILE_SIZE))
    img_name = img.split('.')[0]
    if 'destroy_stage' in img:
        shaders[img_name] = loaded_img
    else:
        block_imgs[img_name] = loaded_img

def light_level_to_color(light_level):
    return (0, 0, 0, (15 - light_level)*17)


def lighting_shader(light_level):
    """Light level from 0 to 15"""
    light_shading = pygame.Surface(BLOCK_TEXTURE_SZ).convert_alpha()
    light_shading.fill(light_level_to_color(light_level))
    return light_shading


light_shaders = [lighting_shader(ll) for ll in range(15)]

BLACK = pygame.Surface(BLOCK_TEXTURE_SZ)
BLACK.fill((0, 0, 0))


def avg_lighting(lights):
    t_light = 0
    n_light = 0
    for value in lights:
        if value:
            t_light += value
            n_light += 1
    if not n_light:
        return 0
    return t_light/n_light


def shade_block(img, light_level):
    if light_level == 15:
        return img.copy()
    shaded_img = img.copy()
    shaded_img.blit(light_shaders[light_level], (0, 0))
    return shaded_img


SHADED_BLOCKS = {}
for block_name in block_imgs:
    img = block_imgs[block_name]
    SHADED_BLOCKS[block_name] = [shade_block(img, ll) for ll in range(16)]

SHADED_BLOCK_CACHE = {}


class Block:

    def __init__(self, pos, block_type, chunk, chunk_coords, visited=False):
        self.pos = pos
        self.type = block_type
        self.x = pos[0]
        self.y = pos[1]
        self.coords = (self.x//TILE_SIZE, self.y//TILE_SIZE)
        self._chunk_coords = chunk_coords
        self.chunk = self.coords[0] >> 3
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        self._damage = -1
        self._visited = visited
        self._light = 0
        self._illumination = 0
        self._chunk = chunk

    @property
    def visited(self):
        return self._visited

    @visited.setter
    def visited(self, value):
        self._visited = value

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        if value < -1:
            value = -1
        if value > 9:
            value = 9
        self._damage = value

    @property
    def light(self):
        """the amount of light of this block is receiving (passive)"""
        return self._light

    @light.setter
    def light(self, value):
        """bounded light setter"""
        self._light = value
        if self._light < 0:
            self._light = 0
        elif self._light > 15:
            self._light = 15

    @property
    def illumination(self):
        """Amount of light this block is emitting."""
        return self._illumination

    @illumination.setter
    def illumination(self, value):
        self._illumination = value
        if self._illumination < 0:
            self._illumination = 0
        elif self._illumination > 15:
            self._illumination = 15

    @property
    def ul_light(self):
        lights = [
                self.light,
                self.left.illumination,
                self.left.above.illumination,
                self.above.illumination
        ]
        return avg_lighting(lights)

    @property
    def ur_light(self):
        lights = [
                self.light,
                self.above.illumination,
                self.above.right.illumination,
                self.right.illumination,
        ]
        return avg_lighting(lights)

    @property
    def lr_light(self):
        lights = [
                self.light,
                self.right.illumination,
                self.right.below.illumination,
                self.below.illumination,
        ]
        return avg_lighting(lights)

    @property
    def ll_light(self):
        lights = [
                self.light,
                self.below.illumination,
                self.below.left.illumination,
                self.left.illumination,
        ]
        return avg_lighting(lights)

    @property
    def img(self):
        if self.type != 'air':
            if not self.light:
                return BLACK

        orig_img = block_imgs[self.type]

        l00 = self.ul_light
        l10 = self.ur_light
        l11 = self.lr_light
        l01 = self.ll_light

        if l00 == l10 == l11 == l01:
            img = SHADED_BLOCKS[self.type][self.light]
        else:

            shaded_block_name = f'{self.type}{l00}{l10}{l11}{l01}'
            if shaded_block_name in SHADED_BLOCK_CACHE:
                return SHADED_BLOCK_CACHE[shaded_block_name]

            colour_rect = pygame.Surface((2, 2)).convert_alpha()
            colour_rect.set_at((0, 0), light_level_to_color(l00))
            colour_rect.set_at((1, 0), light_level_to_color(l10))
            colour_rect.set_at((1, 1), light_level_to_color(l11))
            colour_rect.set_at((0, 1), light_level_to_color(l01))

            colour_rect = pygame.transform.smoothscale(
                colour_rect, BLOCK_TEXTURE_SZ
            )

            img = orig_img.copy()
            img.blit(colour_rect, (0, 0))
            SHADED_BLOCK_CACHE[shaded_block_name] = img

        if self.damage == -1:
            return img

        # apply damage shader
        shaded_img = img.copy()
        shader = shaders[f'destroy_stage_{self.damage}']
        shaded_img.blit(shader, (0, 0))
        return shaded_img

    def get_scrolled_rect(self, scroll):
        rect = pygame.Rect(self.x - scroll[0], self.y - scroll[1], TILE_SIZE, TILE_SIZE)
        return rect

    def get_scrolled_pos(self, scroll):
        pos = (self.x - scroll[0], self.y - scroll[1])
        return pos

    @property
    def above(self):
        """Return the block below this block"""
        return self._chunk[self._chunk_coords[0], self._chunk_coords[1] - 1]

    @property
    def below(self):
        """Return the block below this block"""
        return self._chunk[self._chunk_coords[0], self._chunk_coords[1] + 1]

    @property
    def right(self):
        """Return the block to the right of this block"""
        if self._chunk_coords[0] == CHUNK_SIZE - 1:
            return self._chunk._world.chunks[self.chunk + 1][0, self._chunk_coords[1]]
        return self._chunk[self._chunk_coords[0] + 1, self._chunk_coords[1]]

    @property
    def left(self):
        """Return the block to the right of this block"""
        if self._chunk_coords[0] == 0:
            return self._chunk._world.chunks[self.chunk - 1][CHUNK_SIZE - 1, self._chunk_coords[1]]
        return self._chunk[self._chunk_coords[0] - 1, self._chunk_coords[1]]

    def illumiate(self, light):
        if light > self.light:
            self.light = light

        if self.type == 'air':
            if light > self.illumination:
                self.illumination = light
                self.flood_light()

    def flood_light(self):
        """Light up the surrounding blocks using the flood fill algorithm"""
        self.above.illumiate(self.illumination - 1)
        self.below.illumiate(self.illumination - 1)
        self.left.illumiate(self.illumination - 1)
        self.right.illumiate(self.illumination - 1)
