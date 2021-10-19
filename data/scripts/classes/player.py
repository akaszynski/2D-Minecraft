import logging
import pygame
import os
from math import ceil

from ..core_functions import move, distance
from ...variables import GRAVITY_STRENGTH, TILE_SIZE, CHUNK_SIZE, scroll
from ...blocks import blocks

LOG = logging.getLogger(__name__)


class Player:

    def __init__(
            self, start_pos, width, height, vel, jump_height, reach_distance=4,
            creative=False
    ):

        self._creative = creative
        self.width = width
        self.height = height
        self.vel = vel
        self.jump_height = jump_height
        self.reach_distance = reach_distance

        self.rect = pygame.Rect(start_pos[0]*TILE_SIZE, start_pos[1]*TILE_SIZE,
                                width, height)
        self.coords = (self.rect.x//TILE_SIZE, self.rect.y//TILE_SIZE)
        self.pixel_coords = (self.coords[0] * TILE_SIZE, self.coords[1] * TILE_SIZE)

        self.jumping = False
        self.moving_right = False
        self.moving_left = False
        self.movement = [0, 0]
        self.selected_block = None
        self.current_chunk = 0
        self._previous_chunk = None
        self.inventory = []

        self.current_animation = 'idle'
        self.animations = self.load_animations('data/imgs/player')
        self.animation_counter = 0
        self.animation_flip = False

        # block being interacted by player
        self._current_block = None
        self._current_block_ticks = 0

        # current user tool
        self._current_tool = 'pickaxe'
        self._chunk_changed = False

        self._previous_coords = None

    def move(self, tile_rects):
        
        self.rect, self.collision_types, self.hit_list = move(self.rect, tile_rects, self.movement)

        if self.collision_types['bottom'] and not self.jumping:
            self.movement[1] = 1
        
        if not self.collision_types['bottom']:
            self.jumping = False
            self.movement[1] += GRAVITY_STRENGTH

        if self.collision_types['top']:
            self.movement[1] = 1

        if self.moving_right:
            self.movement[0] = self.vel
            self.current_animation = 'walk'
            self.animation_flip = False
        if self.moving_left:
            self.movement[0] = -self.vel
            self.current_animation = 'walk'
            self.animation_flip = True
        if self.jumping and self.collision_types['bottom']:
            self.movement[1] = -self.jump_height
            self.jumping = False

        if not self.moving_left and not self.moving_right:
            self.movement[0] = 0
            self.current_animation = 'idle'

        if self.movement[1] > 30:
            self.movement[1] = 30

    def get_selected_block(self, terrain, mx, my):
        mx += scroll[0]
        my += scroll[1]
        selected_coords = (mx//TILE_SIZE, my//TILE_SIZE)

        for block in terrain:
            if selected_coords == block.coords:
                if distance(selected_coords, self.coords) <= self.reach_distance:
                    if not block.rect.colliderect(self.rect):
                        self.selected_block = block
                    else:
                        self.selected_block = None
                else:
                    self.selected_block = None

    def reset_break(self, terrain):
        if self._current_block is not None:
            self._current_block.damage = -1
            self._current_block = None

    def break_block(self, terrain, hotbar):
        self.current_animation = 'break'

        # resets block damage shading
        if self._current_block != self.selected_block:
            self.reset_break(terrain)

        if self.selected_block:

            # check if the current block is the selected block
            if self._current_block != self.selected_block:
                self._current_block = self.selected_block
                self._current_block_ticks = 0

            if blocks[self.selected_block.type].hardness == 0:
                # blocks like air or water
                return
            elif blocks[self.selected_block.type].hardness == -1 and not self._creative:
                # bedrock
                return
            elif self._creative:
                tot_ticks = 0
            else:
                # The base time in seconds is the block's hardness
                # multiplied by 1.5 if the player can harvest the
                # block with the current tool, or 5 if the player
                # cannot.

                # base time in ticks is 20 times the above

                # converting to ticks, that's 30
                block = blocks[self.selected_block.type]
                if self._current_tool in block.harvest:
                    tot_ticks = block.hardness*10
                else:
                    tot_ticks = block.hardness*100

            LOG.debug("Breaking block.")
            if tot_ticks:
                self.selected_block.damage = ceil(9*self._current_block_ticks/tot_ticks)
            self._current_block_ticks += 1

            if self._current_block_ticks >= tot_ticks:
                self._break_block(terrain, hotbar)
                self.selected_block.damage = -1

    def _break_block(self, terrain, hotbar):
        if self._current_tool in blocks[self.selected_block.type].harvest:
            block_type = self.selected_block.type
            if block_type in ['grass_block', 'grass_block_snow']:
                block_type = 'dirt'
            if block_type == 'stone':
                block_type = 'cobblestone'
            self.inventory.append(block_type)
            hotbar.add_block_to_slot(block_type, 1)
        terrain.remove_block(self.selected_block.pos)

    def place_block(self, terrain, hotbar):
        self.current_animation = 'place'
        if self.selected_block and self.selected_block.type in ['air', 'water', 'lava']:
            # if self.selected_block and self.selected_block.type == 'tnt':
            #     terrain.remove_block(self.selected_block.pos)
            if hotbar.selected_slot_content != []:
                if hotbar.selected_slot_content[1] > 0:
                    if terrain.add_block(self.selected_block.pos, hotbar.selected_slot_content[0]):
                        hotbar.slot_contents[hotbar.selected_slot][1] -= 1

    def load_animations(self, dir):
        animation_dict = {}
        for animation in os.listdir(dir):
            frame_list = []
            for frame in os.listdir(dir + '/' + animation):
                img = pygame.image.load(dir+'/'+animation+'/'+frame).convert_alpha()
                img = pygame.transform.scale(img, (TILE_SIZE*2-10, TILE_SIZE*2-10))
                frame_list.append(img)
            animation_dict[animation] = frame_list

        return animation_dict

    def draw(self, display):

        if self.animation_counter//7 < len(self.animations[self.current_animation]):
            current_img = self.animations[self.current_animation][self.animation_counter//7]
        else:
            self.animation_counter = 0
            current_img = self.animations[self.current_animation][self.animation_counter//7]
        self.animation_counter += 1

        if self.animation_flip:
            current_img = pygame.transform.flip(current_img, True, False)

        scrolled_pos = (self.rect.x - scroll[0]-30, self.rect.y - scroll[1]+3)
        display.blit(current_img, scrolled_pos)

        if self.selected_block:
            block_rect = pygame.Rect(
                self.selected_block.x - scroll[0],
                self.selected_block.y - scroll[1],
                TILE_SIZE,
                TILE_SIZE
            )
            pygame.draw.rect(display, 'black', block_rect, 3)

    @property
    def _chunk_bounds(self):
        return (self.current_chunk*CHUNK_SIZE, (self.current_chunk + 1)*CHUNK_SIZE)

    def update(self, terrain):
        self.move(terrain.tile_rects)
        self.coords = (self.rect.x//TILE_SIZE, self.rect.y//TILE_SIZE)
        self.pixel_coords = (self.coords[0] * TILE_SIZE, self.coords[1] * TILE_SIZE)

        if self.coords[0] < self._chunk_bounds[0]:
            self.current_chunk -= 1
        elif self.coords[0] > self._chunk_bounds[1]:
            self.current_chunk += 1

        if self.coords != self._previous_coords:
            LOG.debug("Coordinates now (%d, %d)", *self.coords)
            self._previous_coords = self.coords

        if self.current_chunk != self._previous_chunk:
            LOG.debug("Player now at chunk %d", self.current_chunk)
            LOG.debug("Coordinates now (%d, %d)", *self.coords)
            self._previous_chunk = self.current_chunk
            self._chunk_changed = True
        else:
            self._chunk_changed = False

    @property
    def chunk_changed(self):
        """Return if the current chunk changed."""
        return self._chunk_changed
