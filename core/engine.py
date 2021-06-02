"""engine.py
This module holds the core class to run and manage the game at runtime
"""
import shelve
from copy import deepcopy
from os import mkdir

import pyxel

from core import Assets, Draw, Animation, Collision


class ResetManager:
    """ Reset manager to store default state of class for resetting """

    def store(self, cls):
        """
        :param cls: class self parameter to be saved
        """
        self.__dict__ = deepcopy(cls.__dict__)

    def get_stored(self):
        """
        returns a copy of the stored defaults
        """
        return deepcopy(self.__dict__)


RESET_MANAGER = ResetManager()


class Tamagotchi:
    """ Tamagotchi game class manager using Pyxel library as the engine """

    def __init__(self):

        # setup mouse and screen
        self.screen = (100, 100)
        self.room = {'w': self.screen[0], 'h': self.screen[1] - 22, 'current': 3}  # minus the room wall height
        pyxel.init(self.screen[0], self.screen[1], caption="Tamagotchi")
        pyxel.mouse(True)

        # setup character
        self.player = {'x': 0, 'y': 25, 'w': 17, 'h': 22, 'direction': -1}

        # load assets/collisions/animations
        self.collision = Collision()
        self.draw_manager = Draw(collision=self.collision)
        self.animation = Animation()

        # set values to reset
        RESET_MANAGER.store(self)

        # load save game and replace class instance with saved instance
        self._load_save()
        self.room['current'] = 3  # reset to start at menu

    def _load_save(self):
        try:
            save = shelve.open('saves/tamagotchi_save')
            self.__dict__ = save['Tamagotchi'].__dict__ if 'Tamagotchi' in save else self.__dict__
            save.close()
        except FileNotFoundError:
            mkdir('saves')

    def _clear_save(self):
        try:
            save = shelve.open('saves/tamagotchi_save')
            save.clear()
            save.close()
            self.__dict__ = RESET_MANAGER.get_stored()
        except FileNotFoundError:
            pass

    def _save_game(self):
        save = shelve.open('saves/tamagotchi_save')
        save['Tamagotchi'] = self
        save.close()

    def run(self):
        """ Start pyxel engine """
        pyxel.run(self.update, self.draw)

    def check_colliders(self, move_x: int = 0, move_y: int = 0) -> bool:
        """
        Checks collision in future position of player/character
        :param move_x: how many steps to move on the x origin
        :param move_y: how many steps to move on the y origin
        :return: True if colliding else False
        """
        results = self.collision.does_player_collide(
            player_x=self.player['x'] + move_x,
            player_y=self.player['y'] + move_y,
            player_h=self.player['h'],
            player_w=self.player['w']
        )
        return results

    def move_character(self):
        """
        Character movement controller
        """
        self.player['direction'] = -1
        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            if 0 <= self.player['x'] - 1 <= self.room['w'] and not self.check_colliders(move_x=-1):
                self.player['x'] -= 1
                self.player['direction'] = 0
        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            if 0 <= self.player['x'] + 1 <= self.room['w'] - self.player['w'] and not self.check_colliders(move_x=1):
                self.player['x'] += 1
                self.player['direction'] = 1
        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            if 0 <= self.player['y'] - 1 <= self.room['h'] and not self.check_colliders(move_y=-1):
                self.player['y'] -= 1
                self.player['direction'] = 2
        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            if 0 <= self.player['y'] + 1 <= self.room['h'] and not self.check_colliders(move_y=1):
                self.player['y'] += 1
                self.player['direction'] = 3

    def menu_pressed(self):
        """
        Check if left mouse button pressed position falls within menu button and calls correct logic
        """
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and self.draw_manager.menu.mouse_over_menu(menu_btn=Assets.PLAY_2):
            self.draw_manager.menu.play(sound='play')
            self.room['current'] = 0
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and self.draw_manager.menu.mouse_over_menu(menu_btn=Assets.QUIT_2):
            self.draw_manager.menu.play(sound='quit')
            pyxel.quit()
        if pyxel.btnp(pyxel.MOUSE_LEFT_BUTTON) and self.draw_manager.menu.mouse_over_menu(menu_btn=Assets.RESET_2):
            self.draw_manager.menu.play(sound='reset')
            self._clear_save()

    def change_room(self):
        """
        Game room change controller
        rooms = 0:bedroom, 1:kitchen, 2:bathroom
        """
        if pyxel.btnp(pyxel.KEY_1):
            self.room['current'] = 0
        if pyxel.btnp(pyxel.KEY_2):
            self.room['current'] = 1
        if pyxel.btnp(pyxel.KEY_3):
            self.room['current'] = 2

    def update(self):
        """ Game logic """
        if self.room['current'] == 3:
            self.menu_pressed()
        else:
            self.move_character()
            self.change_room()

        if pyxel.btnp(pyxel.KEY_Q):
            self.room['current'] = 3
            self._save_game()

    def draw(self):
        """ Pyxel update screen changes """
        # clear screen
        pyxel.cls(0)

        # draw assets in current room
        self.draw_manager.draw_room(room=self.room['current'])

        # # draw player
        if self.room['current'] != 3:
            frame = self.animation.get_walk_animation(direction=self.player['direction'])
            self.draw_manager.draw_player(x=self.player['x'], y=self.player['y'], frame=frame)
