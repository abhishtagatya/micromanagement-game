from typing import Dict
from micromanagement.game_obj import Map
from micromanagement.game_obj.map import (
    MAP_LVL_1, MAP_LVL_2, MAP_LVL_3, MAP_LVL_4, MAP_LVL_5
)


class GameLevel:
    STATE_RECORDING = 'recording'

    def __init__(self, tile_set: Dict):
        self.level = 0
        self.level_map = [
            # (MAP_LVL_1, 10),
            # (MAP_LVL_2, 15),
            # (MAP_LVL_3, 20),
            # (MAP_LVL_4, 35),
            (MAP_LVL_5, 50),
        ]

        self.map_obj = Map(tile_set, layout_preset=self.level_map[self.level][0])
        self.max_steps = self.level_map[self.level][1]
        self.state = {self.STATE_RECORDING: False}

    def step(self):
        self.max_steps -= 1
        return self.max_steps

    def add_step(self, inc=5):
        self.max_steps += inc
        return self.max_steps

    def update_state(self, key, value):
        self.state[key] = value
        return self.state

    def get_state(self, key):
        return self.state[key]

    def level_up(self):
        self.level += 1
        if self.level < len(self.level_map):
            self.map_obj = Map(self.map_obj.tile_set, layout_preset=self.level_map[self.level][0])
            self.max_steps = self.level_map[self.level][1]
            return True
        return False

    def reset_level(self):
        self.map_obj = Map(self.map_obj.tile_set, layout_preset=self.level_map[self.level][0])
        self.max_steps = self.level_map[self.level][1]

    def reset_map(self):
        self.level = 0
        self.map_obj = Map(self.map_obj.tile_set, layout_preset=self.level_map[self.level][0])
        self.max_steps = self.level_map[self.level][1]
        self.state = {self.STATE_RECORDING: False}

    def get_layout(self):
        return self.map_obj.layout

    def draw_tile(self, row, col, tile, screen):
        return self.map_obj.draw_tile(row, col, tile, screen)

    def update_tile(self, key, value):
        self.map_obj.tile_set[key] = value
        return

    def move_object(self, current_coord, desired_coord):
        return self.map_obj.move_tile(current_coord, desired_coord)

    def remove_object(self, coord):
        return self.map_obj.remove_tile(coord)

    def obstacle_count(self):
        return self.map_obj.obstacle_count
