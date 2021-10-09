
import os

import pygame

from ...variables import STACK_SIZE
from ..core_functions import draw_rect_alpha

block_imgs_dir = 'data/imgs/blocks'
imgs_dir = 'data/imgs'
inv_path = os.path.join(imgs_dir, 'inventory.png')

font = pygame.font.Font('data/fonts/minecraft_font.ttf', 23)


class Inventory:

    def __init__(self, window_size):
        self._show = False

        # location of the bottom right corner of inventory in png
        inv_png_sz = (175, 165)
        total_sz = (255, 255)

        dim = int(min(window_size)//1.5)
        self.width = int(dim*(inv_png_sz[0]/inv_png_sz[1]))
        self.height = int(dim/(inv_png_sz[0]/inv_png_sz[1]))

        self.x = window_size[0]//2 - self.width//2
        self.y = window_size[1] - window_size[1]//1.2
        self.selected_slot = 1

        inv_img = pygame.image.load(inv_path).convert_alpha()
        scale_x = total_sz[0]/inv_png_sz[0]
        scale_y = total_sz[0]/inv_png_sz[1]
        inv_img = pygame.transform.scale(inv_img, (int(self.width*scale_x),
                                                   int(self.height*scale_y)))

        self._inv_surf = pygame.Surface((self.width, self.height))
        self._inv_surf.blit(inv_img, (0, 0), (0, 0,
                                              int(self.width),
                                              int(self.height)))

        # location of first hotbar square
        slot_bar_png_top_left = (8, 142)
        slot_bar_png_bot_right = (23, 157)
        
        # each shifted right by two pixels
        block_sz = int(22*(self.width/255))
        tot_scale_x = scale_x*self.width/255
        tot_scale_y = scale_y*self.height/255

        block_imgs = {}
        for img in os.listdir(block_imgs_dir):
            loaded_img = pygame.image.load(block_imgs_dir + '/' + img).convert_alpha()
            loaded_img = pygame.transform.scale(loaded_img, (block_sz, block_sz))
            img_name = img.split('.')[0]
            block_imgs[img_name] = loaded_img

        # self._inv_surf.blit(block_imgs['leaf'],
        #                     (8*tot_scale_x, 142*tot_scale_y),
        #                     (0, 0, block_sz, block_sz))


        # self.slot_width = self.width//9
        # self.slot_height = self.slot_width

        # self.base_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # self.slot_rects = {}
        # x = self.x
        # for i in range(9):
        #     rect = pygame.Rect(x, self.y, self.slot_width, self.slot_height)
        #     self.slot_rects[i+1] = rect
        #     x += self.slot_width

        # self.slot_contents = {
        #         1: [],
        #         2: [],
        #         3: [],
        #         4: [],
        #         5: [],
        #         6: [],
        #         7: [],
        #         8: [],
        #         9: []
        #     }

        # self.block_preview_imgs = {}
        # for img in os.listdir(imgs_dir):
        #     loaded_img = pygame.image.load(imgs_dir + '/' + img).convert_alpha()
        #     loaded_img = pygame.transform.scale(loaded_img, (self.slot_width-10, self.slot_height-10))
        #     img_name = img.split('.')[0]
        #     self.block_preview_imgs[img_name] = loaded_img

    # def get_available_slot(self, block_type):
    #     # First check if there is a slot which the item can be added with another item
    #     for i, n in self.slot_contents.items():
    #         if n != []:
    #             if n[0] == block_type and n[1] < STACK_SIZE:
    #                 return i

    #     # If not, returns the first available slot
    #     for i, n in self.slot_contents.items():
    #         if n == []:
    #             return i

    # def add_block_to_slot(self, block_type, amount):
    #     slot = self.get_available_slot(block_type)
    #     if self.slot_contents[slot] == []:
    #         self.slot_contents[slot] = [block_type, amount]
    #     else:
    #         self.slot_contents[slot][1] += amount

    @property
    def visible(self):
        return self._show

    def toggle(self):
        self._show = not self._show

    def draw(self, display):
        if self._show:
            self._draw(display)

    def _draw(self, display):
        display.blit(self._inv_surf, (self.x, self.y))
        # display.blit(inv_img, (0, 0), (0, 0, 400, 400))
        # draw_rect_alpha(display, (0, 0, 0, 50), self._inv_surf)
        # self._inv_surf
        # display.blit(
    #     for index, rect in self.slot_rects.items():
    #         if index != self.selected_slot:
    #             pygame.draw.rect(display, (25, 25, 25), rect, 4)
    #     # Drawing selected slot after the rest so that it is drawn on top of other slots
    #     pygame.draw.rect(display, (200, 200, 200), self.slot_rects[self.selected_slot], 5)

    #     for i, n in self.slot_contents.items():
    #         if n != []:
    #             centering_rect = self.block_preview_imgs[n[0]].get_rect()
    #             centering_rect.center = self.slot_rects[i].center
    #             display.blit(self.block_preview_imgs[n[0]], centering_rect.topleft)

    #             if n[1] > 1:
    #                 font_render = font.render(str(n[1]), True, (200, 200, 200))
    #                 font_centering_rect = font_render.get_rect()
    #                 font_centering_rect.bottomright = centering_rect.bottomright
    #                 display.blit(font_render, font_centering_rect.topleft)

    # def update(self):
    #     self.selected_slot_content = self.slot_contents[self.selected_slot]
    #     for i, n in self.slot_contents.items():
    #         if n != []:
    #             if n[1] <= 0:
    #                 self.slot_contents[i] = []
