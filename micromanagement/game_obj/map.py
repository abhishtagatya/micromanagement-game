import copy
from typing import List, Dict


class Map:
    BARRIER_L = 'L'  # Left
    BARRIER_R = 'R'  # Right
    BARRIER_U = 'U'  # Up
    BARRIER_D = 'D'  # Down

    BARRIER_Q = 'Q'  # Top Left
    BARRIER_E = 'E'  # Top Right
    BARRIER_Z = 'Z'  # Down Left
    BARRIER_C = 'C'  # Down Right

    BARRIER_X = 'X'

    PLAYER = 'A'
    BOX = 'B'
    GOAL = 'O'
    EMPTY = ' '

    SCREEN_HEIGHT = 800
    SCREEN_WIDTH = 600
    TILE_WIDTH = 40
    TILE_HEIGHT = 40
    TOP_OFFSET = 0

    def __init__(self, tile_set: Dict, layout_preset: List = None):
        self.tile_set = tile_set

        self.layout = None
        if layout_preset:
            self.layout = copy.deepcopy(layout_preset)

        self.collider = [
            self.BARRIER_L, self.BARRIER_R, self.BARRIER_U, self.BARRIER_D,
            self.BARRIER_Q, self.BARRIER_E, self.BARRIER_Z, self.BARRIER_C,
            self.BARRIER_X, self.BOX
        ]

        self.removable = [
            self.BOX
        ]

        self.obstacle_count = self.count_obstacle()

    def count_obstacle(self):
        obstacle = 0
        for r in self.layout:
            for c in r:
                if c == self.BOX:
                    obstacle += 1
        return obstacle

    def draw_tile(self, row, col, tile, screen):
        image = self.tile_set.get(tile, None)

        if image is None:
            return

        rect = image.get_rect()
        rect.topleft = (col * self.TILE_WIDTH, row * self.TILE_HEIGHT + self.TOP_OFFSET)

        screen.blit(self.tile_set[tile], (rect.x, rect.y))

    def _check_collision(self, x, y):
        if self.layout[x][y] in self.collider:
            return True
        return False

    def _check_block(self, x, y):
        return self.layout[x][y]

    def move_tile(self, current, moving):

        c_x, c_y = current
        m_x, m_y = moving

        if not self._check_collision(m_x, m_y):
            self.layout[m_x][m_y] = self.PLAYER
            self.layout[c_x][c_y] = self.EMPTY
            return True
        return False

    def remove_tile(self, selected):
        s_x, s_y = selected

        if self._check_block(s_x, s_y) in self.removable:
            self.layout[s_x][s_y] = self.EMPTY
            self.obstacle_count = self.count_obstacle()
            return True
        return False


MAP_LVL_1 = [
    ['Q', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'E'],
    ['L', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'R'],
    ['L', 'X', 'A', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', 'X', 'R'],
    ['L', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'R'],
    ['Z', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C']]

MAP_LVL_2 = [
    ['Q', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'E'],
    ['L', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'R'],
    ['L', 'X', 'B', ' ', ' ', ' ', 'A', ' ', ' ', ' ', ' ', ' ', 'B', 'X', 'R'],
    ['L', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'R'],
    ['Z', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C']]

MAP_LVL_3 = [
    ['Q', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'E'],
    ['L', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', ' ', ' ', ' ', 'R'],
    ['L', 'X', 'B', ' ', ' ', ' ', 'A', ' ', ' ', 'X', ' ', ' ', 'B', ' ', 'R'],
    ['L', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', 'R'],
    ['L', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'X', 'X', ' ', ' ', ' ', ' ', 'R'],
    ['L', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'R'],
    ['L', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'R'],
    ['L', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'R'],
    ['Z', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C']]

MAP_LVL_4 = [
    ['Q', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'E'],
    ['L', 'B', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'R'],
    ['L', ' ', 'X', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'R'],
    ['L', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'R'],
    ['L', ' ', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', ' ', 'A', 'R'],
    ['L', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'R'],
    ['L', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'R'],
    ['L', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'R'],
    ['L', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'R'],
    ['Z', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C']]

MAP_LVL_5 = [
    ['Q', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'E'],
    ['L', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'B', 'R'],
    ['L', ' ', 'A', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'R'],
    ['L', 'X', 'X', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'R'],
    ['L', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'R'],
    ['L', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'R'],
    ['L', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X', 'X', 'X', ' ', 'X', ' ', 'R'],
    ['L', ' ', ' ', ' ', 'X', ' ', ' ', ' ', 'X', 'B', 'X', 'X', 'X', ' ', 'R'],
    ['L', ' ', ' ', ' ', 'X', 'B', ' ', ' ', 'X', ' ', 'X', ' ', 'X', ' ', 'R'],
    ['L', ' ', ' ', ' ', 'X', 'X', 'X', 'X', 'X', ' ', 'X', ' ', 'X', ' ', 'R'],
    ['L', ' ', ' ', ' ', ' ', ' ', 'B', 'X', ' ', ' ', ' ', ' ', 'X', ' ', 'R'],
    ['L', 'B', ' ', ' ', ' ', ' ', ' ', 'B', ' ', ' ', ' ', ' ', 'X', 'B', 'R'],
    ['Z', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C']]

MAP_LT_Y = [
    ['Q', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'U', 'E'],
    ['L', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'R'],
    ['L', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'R'],
    ['L', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'R'],
    ['L', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'R'],
    ['L', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', 'X', 'X', 'X', ' ', 'R'],
    ['L', ' ', 'X', 'B', 'X', ' ', ' ', ' ', ' ', ' ', 'X', 'B', 'X', ' ', 'R'],
    ['L', ' ', 'X', 'X', 'X', 'X', 'X', 'X', ' ', ' ', 'X', ' ', 'X', ' ', 'R'],
    ['L', ' ', ' ', ' ', 'X', ' ', 'B', 'X', ' ', ' ', 'X', ' ', 'X', ' ', 'R'],
    ['L', ' ', ' ', ' ', 'X', ' ', 'X', 'X', ' ', ' ', 'X', ' ', 'X', ' ', 'R'],
    ['L', ' ', ' ', ' ', 'X', ' ', ' ', 'X', ' ', ' ', ' ', ' ', 'X', ' ', 'R'],
    ['L', ' ', ' ', ' ', ' ', ' ', ' ', 'X', ' ', ' ', ' ', ' ', 'X', 'A', 'R'],
    ['Z', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'C']]
