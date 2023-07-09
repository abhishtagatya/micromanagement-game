import sys
import base64
import os.path
from pathlib import Path
import webbrowser

from micromanagement.game_mechanic import (
    AudioMechanic, TranscriptMechanic, TextGenerationMechanic, MovementMechanic
)

from micromanagement.game_obj import Map, GameLevel
from micromanagement.game_ui import Button

import pygame as pg


class MicroManageGame:

    OUTPUT_PATH = Path(__file__).parent
    ASSETS_PATH = OUTPUT_PATH / Path("assets")

    def __init__(self):
        self.secret = self.load_secret()
        self.audio_mechanic = AudioMechanic(filename=self.relative_to_assets('output.wav').__str__())
        self.transcript_mechanic = TranscriptMechanic(token=self.secret)
        self.generate_mechanic = TextGenerationMechanic(token=self.secret)
        self.movement_mechanic = MovementMechanic()

        self.url_plug = "https://github.com/abhishtagatya"

        icon_image = pg.image.load(self.relative_to_assets('Icon_Image.png'))
        self.screen = pg.display.set_mode((Map.SCREEN_WIDTH, Map.SCREEN_HEIGHT))
        pg.display.set_caption(title='Micro Management v1.0')
        pg.display.set_icon(icon_image)

        pg.font.init()
        self.pixel_font = pg.font.Font(self.relative_to_assets("I-pixel-u.ttf"), 20)

        pg.mixer.init()
        pg.mixer.music.load(self.relative_to_assets('mixkit-game-level-music-689.wav'))
        self.fixing_sound = pg.mixer.Sound(self.relative_to_assets('extra-vg.wav'))

        mic_off_btn = pg.image.load(self.relative_to_assets('Mic_Off.png')).convert_alpha()
        mic_on_btn = pg.image.load(self.relative_to_assets('Mic_On.png')).convert_alpha()
        self.mic_button = Button(20, 650, mic_off_btn, alternate_image=mic_on_btn, scale=1)

        reset_btn = pg.image.load(self.relative_to_assets('RESET_LEVEL.png')).convert_alpha()
        self.reset_button = Button(420, 520, reset_btn)

        barrier_l_image = pg.image.load(self.relative_to_assets('Barrier_Left.png')).convert_alpha()
        barrier_r_image = pg.image.load(self.relative_to_assets('Barrier_Right.png')).convert_alpha()
        barrier_u_image = pg.image.load(self.relative_to_assets('Barrier_Up.png')).convert_alpha()
        barrier_d_image = pg.image.load(self.relative_to_assets('Barrier_Down.png')).convert_alpha()

        barrier_ul_image = pg.image.load(self.relative_to_assets('Barrier_CLU.png')).convert_alpha()
        barrier_ur_image = pg.image.load(self.relative_to_assets('Barrier_CRU.png')).convert_alpha()
        barrier_dl_image = pg.image.load(self.relative_to_assets('Barrier_DLU.png')).convert_alpha()
        barrier_dr_image = pg.image.load(self.relative_to_assets('Barrier_DRU.png')).convert_alpha()

        barrier_x_image = pg.image.load(self.relative_to_assets('Beam_Blue.png')).convert_alpha()

        start_off_btn = pg.image.load(self.relative_to_assets('Start_Button.png')).convert_alpha()
        support_off_btn = pg.image.load(self.relative_to_assets('Support_Button.png')).convert_alpha()
        exit_off_btn = pg.image.load(self.relative_to_assets('Exit_Button.png')).convert_alpha()

        title_btn = pg.image.load(self.relative_to_assets('Title.png')).convert_alpha()
        title_drop_btn = pg.image.load(self.relative_to_assets('Title_Drop.png')).convert_alpha()

        win_title_btn = pg.image.load(self.relative_to_assets('Win_Title.png')).convert_alpha()
        lose_title_btn = pg.image.load(self.relative_to_assets('Lose_Title.png')).convert_alpha()

        self.title_button = Button(60, 150, title_btn, alternate_image=title_drop_btn, scale=1)
        self.win_button = Button(110, 150, win_title_btn, scale=1)
        self.lose_button = Button(110, 150, lose_title_btn, scale=1)

        self.start_button = Button(550 - 180 + 60, 350, start_off_btn, scale=1)
        self.support_button = Button(550 - 180, 420, support_off_btn, scale=1)
        self.exit_button = Button(550 - 180 + 60, 490, exit_off_btn, scale=1)
        self.exit_c_button = Button(240, 470, exit_off_btn, scale=1)

        self.character_down_img = pg.image.load(self.relative_to_assets('Character_Down.png')).convert_alpha()
        self.character_up_img = pg.image.load(self.relative_to_assets('Character_Up.png')).convert_alpha()
        self.character_left_img = pg.image.load(self.relative_to_assets('Character_Left.png')).convert_alpha()
        self.character_right_img = pg.image.load(self.relative_to_assets('Character_Right.png')).convert_alpha()

        box_img = pg.image.load(self.relative_to_assets('Box_Blue.png')).convert_alpha()
        goal_img = pg.image.load(self.relative_to_assets('Goal_Blue.png')).convert_alpha()

        self.scalar = 1
        self.game_level = GameLevel(
            tile_set={
                Map.BARRIER_L: pg.transform.scale(barrier_l_image,
                                                  (int(Map.TILE_WIDTH * self.scalar),
                                                   int(Map.TILE_HEIGHT * self.scalar))),
                Map.BARRIER_R: pg.transform.scale(barrier_r_image,
                                                  (int(Map.TILE_WIDTH * self.scalar),
                                                   int(Map.TILE_HEIGHT * self.scalar))),
                Map.BARRIER_U: pg.transform.scale(barrier_u_image,
                                                  (int(Map.TILE_WIDTH * self.scalar),
                                                   int(Map.TILE_HEIGHT * self.scalar))),
                Map.BARRIER_D: pg.transform.scale(barrier_d_image,
                                                  (int(Map.TILE_WIDTH * self.scalar),
                                                   int(Map.TILE_HEIGHT * self.scalar))),

                Map.BARRIER_Q: pg.transform.scale(barrier_ul_image,
                                                  (int(Map.TILE_WIDTH * self.scalar),
                                                   int(Map.TILE_HEIGHT * self.scalar))),
                Map.BARRIER_E: pg.transform.scale(barrier_ur_image,
                                                  (int(Map.TILE_WIDTH * self.scalar),
                                                   int(Map.TILE_HEIGHT * self.scalar))),
                Map.BARRIER_Z: pg.transform.scale(barrier_dl_image,
                                                  (int(Map.TILE_WIDTH * self.scalar),
                                                   int(Map.TILE_HEIGHT * self.scalar))),
                Map.BARRIER_C: pg.transform.scale(barrier_dr_image,
                                                  (int(Map.TILE_WIDTH * self.scalar),
                                                   int(Map.TILE_HEIGHT * self.scalar))),

                Map.BARRIER_X: pg.transform.scale(barrier_x_image,
                                                  (int(Map.TILE_WIDTH * self.scalar),
                                                   int(Map.TILE_HEIGHT * self.scalar))),

                Map.PLAYER: pg.transform.scale(self.character_down_img,
                                               (int(Map.TILE_WIDTH * self.scalar), int(Map.TILE_HEIGHT * self.scalar))),
                Map.BOX: pg.transform.scale(box_img,
                                            (int(Map.TILE_WIDTH * self.scalar), int(Map.TILE_HEIGHT * self.scalar))),
                Map.GOAL: pg.transform.scale(goal_img,
                                             (int(Map.TILE_WIDTH * self.scalar), int(Map.TILE_HEIGHT * self.scalar))),
            }
        )

        pg.mixer.music.play(-1)

    @staticmethod
    def relative_to_assets(fpath: str) -> str:
        bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__))) + '/assets'
        bundle_path = os.path.abspath(os.path.join(bundle_dir, fpath)).__str__()
        return bundle_path

    @staticmethod
    def load_secret():
        print('Pwd: ', os.getcwd())
        print('Checking Assets: ', os.listdir(MicroManageGame.relative_to_assets('')))
        if os.path.exists(MicroManageGame.relative_to_assets('secrets.txt')):
            with open(MicroManageGame.relative_to_assets('secrets.txt')) as sec_file:
                sec_content = sec_file.read()
                sec_decode = base64.b64decode(sec_content).decode('utf-8')
                return sec_decode
        raise FileNotFoundError('File not found. "secrets.txt"')

    def run(self):
        opt = 'MENU'
        progress = None
        level_up = None
        while True:
            while opt == 'MENU':
                self.screen.fill((32, 21, 51))
                self.title_button.draw(self.screen)
                if self.start_button.draw(self.screen):
                    opt = 'START'
                    break
                if self.support_button.draw(self.screen):
                    opt = 'SUPPORT'
                    break
                if self.exit_button.draw(self.screen) or opt == 'EXIT':
                    opt = 'EXIT'
                    break

                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        opt = 'EXIT'
                pg.display.update()

            if opt == 'START':
                game_opt, progress = self.game_run()
                if game_opt == 'GAME':
                    if progress:
                        level_up = self.game_level.level_up()

                        if not level_up:
                            opt = 'WIN'
                    else:
                        opt = 'LOSE'
                else:
                    opt = 'MENU'

            if opt == 'WIN':
                opt = self.end_screen(win=True)
                self.game_level.reset_map()
                progress = None
                level_up = None

            if opt == 'LOSE':
                opt = self.end_screen()
                self.game_level.reset_map()
                progress = None
                level_up = None

            if opt == 'SUPPORT':
                webbrowser.open(self.url_plug)
                break

            if opt == 'EXIT':
                pg.quit()
                break

        pg.quit()

    def end_screen(self, win=False):
        opt = None
        while opt is None:
            self.screen.fill((32, 21, 51))
            if win:
                self.win_button.draw(self.screen)
            else:
                self.lose_button.draw(self.screen)

            if self.exit_c_button.draw(self.screen):
                opt = 'MENU'
                break

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    opt = 'EXIT'
                    break
            pg.display.update()
        return opt

    def game_run(self):
        opt = 'GAME'
        player_pos = (0, 0)
        player_score = self.game_level.max_steps
        self.movement_mechanic.clear()

        run = True
        progress = False

        prompt_text = "Ask Micheal to Fix the Boxes Nearby"
        while run:
            self.screen.fill((32, 21, 51))
            score_text = self.pixel_font.render(f"REMAINING STEPS: {player_score}", True, (255, 255, 255))
            self.screen.blit(score_text, (20, 520))

            if len(prompt_text) > 40:
                up_text = prompt_text[:35]
                down_text = prompt_text[35:]
            else:
                up_text = prompt_text
                down_text = ""

            previous_up_command = self.pixel_font.render(f"\"{up_text.upper()}\"", True, (255, 255, 255))
            self.screen.blit(previous_up_command, (20, 560))
            if down_text != "":
                previous_down_command = self.pixel_font.render(f"\"{down_text.upper()}\"", True, (255, 255, 255))
                self.screen.blit(previous_down_command, (20, 600))

            if self.game_level.max_steps < 1:
                run = False

            if self.game_level.obstacle_count() < 1:
                run = False
                progress = True

            if self.mic_button.draw(self.screen):
                self.game_level.update_state(GameLevel.STATE_RECORDING, True)
                self.mic_button.disable()
            else:
                self.mic_button.enable()

            if self.reset_button.draw(self.screen):
                self.game_level.reset_level()
                player_score = self.game_level.max_steps

            for i, row in enumerate(self.game_level.get_layout()):
                for j, col in enumerate(row):

                    if col == self.game_level.map_obj.PLAYER:
                        player_pos = (i, j)

                    self.game_level.draw_tile(i, j, col, self.screen)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                    opt = 'MENU'

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        run = False
                        opt = 'MENU'

            current_pos = player_pos
            next_move = self.movement_mechanic.pop()
            if next_move == self.movement_mechanic.K_UP:
                moving_pos = (player_pos[0] - 1, player_pos[1])
                self.game_level.update_tile(Map.PLAYER, pg.transform.scale(
                    self.character_up_img, (int(Map.TILE_WIDTH * self.scalar), int(Map.TILE_HEIGHT * self.scalar))
                ))
                if self.game_level.move_object(current_pos, moving_pos):
                    player_score = self.game_level.step()
                    pg.time.wait(100)
            elif next_move == self.movement_mechanic.K_DOWN:
                moving_pos = (player_pos[0] + 1, player_pos[1])
                self.game_level.update_tile(Map.PLAYER, pg.transform.scale(
                    self.character_down_img, (int(Map.TILE_WIDTH * self.scalar), int(Map.TILE_HEIGHT * self.scalar))
                ))
                if self.game_level.move_object(current_pos, moving_pos):
                    player_score = self.game_level.step()
                    pg.time.wait(100)
            elif next_move == self.movement_mechanic.K_LEFT:
                moving_pos = (player_pos[0], player_pos[1] - 1)
                self.game_level.update_tile(Map.PLAYER, pg.transform.scale(
                    self.character_left_img, (int(Map.TILE_WIDTH * self.scalar), int(Map.TILE_HEIGHT * self.scalar))
                ))
                if self.game_level.move_object(current_pos, moving_pos):
                    player_score = self.game_level.step()
                    pg.time.wait(100)
            elif next_move == self.movement_mechanic.K_RIGHT:
                moving_pos = (player_pos[0], player_pos[1] + 1)
                self.game_level.update_tile(Map.PLAYER, pg.transform.scale(
                    self.character_right_img, (int(Map.TILE_WIDTH * self.scalar), int(Map.TILE_HEIGHT * self.scalar))
                ))
                if self.game_level.move_object(current_pos, moving_pos):
                    player_score = self.game_level.step()
                    pg.time.wait(100)
            elif next_move == self.movement_mechanic.K_SPACE:
                if self.game_level.remove_object((player_pos[0] + 1, player_pos[1])):
                    self.fixing_sound.play()
                    player_score = self.game_level.add_step()
                if self.game_level.remove_object((player_pos[0] - 1, player_pos[1])):
                    self.fixing_sound.play()
                    player_score = self.game_level.add_step()
                if self.game_level.remove_object((player_pos[0], player_pos[1] + 1)):
                    self.fixing_sound.play()
                    player_score = self.game_level.add_step()
                if self.game_level.remove_object((player_pos[0], player_pos[1] - 1)):
                    self.fixing_sound.play()
                    player_score = self.game_level.add_step()
                pg.time.wait(100)
            pg.display.update()

            if self.game_level.get_state(GameLevel.STATE_RECORDING):
                self.audio_mechanic.record()
                prompt_text = self.transcript_mechanic.transcribe(
                    in_file=self.relative_to_assets('output.wav'),
                    out_file=self.relative_to_assets('output.mp3')
                )
                gen_instruct = self.generate_mechanic.generate(prompt_text)
                self.movement_mechanic.add_from_string(gen_instruct)
                self.game_level.update_state(GameLevel.STATE_RECORDING, False)
        return opt, progress
