import pygame
import os

from ...variables import TILE_SIZE

pygame.init()
pygame.display.set_mode()


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


class Block:

    def __init__(self, pos, block_type):
        self.pos = pos
        self.type = block_type
        self.x = pos[0]
        self.y = pos[1]
        self.coords = (self.x//TILE_SIZE, self.y//TILE_SIZE)
        self.chunk = (self.coords[0] >> 3, self.coords[1] >> 3)
        self.rect = pygame.Rect(self.x, self.y, TILE_SIZE, TILE_SIZE)
        self._damage = -1
        self._visible = True

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
    def img(self):
        if not self.visible:
            return block_imgs['black']
        img = block_imgs[self.type]
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
    def visible(self):
        return self._visible
