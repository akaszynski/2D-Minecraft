from random import randint

import pygame

GRAVITY_STRENGTH = 1
MAX_HEIGHT = 128
CHUNK_SIZE = 8  # Measured in blocks. I do not recommend changing this
TILE_SIZE = 64  # Measured in pixels
SCROLL_STIFF = 8 # How closely the camera follows the player (higher number = less stiff)
RENDER_DISTANCE = 2  # Measured in chunks
STACK_SIZE = 64 # Max number of blocks held in an inventory slot

scroll = [0, 0]
SEED = randint(1, 99999)
