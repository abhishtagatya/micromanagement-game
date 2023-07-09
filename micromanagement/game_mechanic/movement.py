import json
import random


class MovementMechanic:
    K_UP = "K_UP"
    K_LEFT = "K_LEFT"
    K_DOWN = "K_DOWN"
    K_RIGHT = "K_RIGHT"
    K_SPACE = "K_SPACE"
    K_EMPTY = ""

    def __init__(self):
        self.movement_list = []
        self.move_bank = [self.K_UP, self.K_LEFT, self.K_DOWN, self.K_RIGHT, self.K_SPACE]

    def add_from_string(self, moveset_str, scramble=0.05):
        try:
            moveset_json = json.loads(moveset_str)
            for move in moveset_json:
                rng_hit = random.randint(0, 100) < scramble * 100
                if move in self.move_bank:
                    self.movement_list.append(move)

                if rng_hit:
                    self.movement_list.append(random.choice(self.move_bank))

        except json.decoder.JSONDecodeError:
            return

    def pop(self):
        if self.movement_list:
            return self.movement_list.pop(0)
        return self.K_EMPTY

    def clear(self):
        self.movement_list = []
