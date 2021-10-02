import logging
import time
import sys

import pygame

from data.scripts.classes.player import Player
from data.scripts.classes.terrain import Terrain
from data.scripts.classes.hotbar import Hotbar

from data.scripts.core_functions import draw, distance
from data.variables import (
    TILE_SIZE, scroll, SCROLL_STIFF, RENDER_DISTANCE
)

MIN_ACTION_TIME = 0.05  # effectively 20 ticks

LOG = logging.getLogger(__name__)
LOG.setLevel('DEBUG')


def process_actions(player, terrain, hotbar):
    """Process all actions"""
    # LOG.debug('Process action')

    #######################################################################
    # get held buttons (for setting and breaking blocks

    mouse_held = pygame.mouse.get_pressed()
    if mouse_held[0]:  # left click for placing
        player.place_block(terrain, hotbar)
    elif mouse_held[2]:  # right click for breaking
        player.break_block(terrain, hotbar)
    else:
        player.reset_break(terrain)

    #######################################################################

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            # control Q to exit
            if event.key == pygame.K_q:
                if pygame.key.get_mods() and pygame.KMOD_CTRL:
                    pygame.quit()
                    sys.exit()

            if event.key == pygame.K_a:
                player.moving_left = True
            if event.key == pygame.K_d:
                player.moving_right = True
            if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                player.jumping = True

            try:
                if int(pygame.key.name(event.key)) != 0:
                    hotbar.selected_slot = int(pygame.key.name(event.key))
            except ValueError:
                pass

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                player.moving_right = False
            if event.key == pygame.K_a:
                player.moving_left = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if event.button == 4:
                if hotbar.selected_slot != 9:
                    hotbar.selected_slot += 1
                else:
                    hotbar.selected_slot = 1

            if event.button == 5:
                if hotbar.selected_slot != 1:
                    hotbar.selected_slot -= 1
                else:
                    hotbar.selected_slot = 9



def main(full_screen=False, window_size=None):
    """Main program loop.

    Parameters
    ----------
    full_screen : bool
        Run pygame in full screen.
    window_size : tuple
        Size of the window in ``(x, y)``

    """
    pygame.init()

    clock = pygame.time.Clock()

    if full_screen:
        raise NotImplementedError('Full screen not implemented')

    if window_size is None:
        # still windowed and not genuinely full screen
        info = pygame.display.Info()
        window_size = info.current_w, info.current_h - 50

    screen = pygame.display.set_mode(window_size)

    player = Player((0, -200), TILE_SIZE-10, TILE_SIZE*2-10, 9, 13)
    hotbar = Hotbar(window_size)
    terrain = Terrain()
    terrain.generate_chunk(0, 0)

    last_action_time = 0
    while True:
        clock.tick(60)
        pygame.display.set_caption(str(int(clock.get_fps())))

        time_since_last_action = time.time() - last_action_time
        if time_since_last_action > MIN_ACTION_TIME:
            process_actions(player, terrain, hotbar)
            last_action_time = time.time()

        mx, my = pygame.mouse.get_pos()

        scroll[0] += int(
            (player.rect.x - scroll[0] - (window_size[0]/2 + player.width/2 - 50)) / SCROLL_STIFF
        )
        scroll[1] += int(
            (player.rect.y - scroll[1] - (window_size[1]/2 + player.height/2 - 100)) / SCROLL_STIFF
        )

        for chunk in list(set([i.chunk for i in terrain.map])):
            if distance(player.current_chunk, chunk) >= RENDER_DISTANCE:
                terrain.unload_chunk(chunk)

        player.get_selected_block(terrain, mx, my)

        terrain.update(player)
        player.update(terrain)
        hotbar.update()

        draw(screen, terrain, player, hotbar)
