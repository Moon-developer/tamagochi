"""colliders.py
This module holds the classes required to manage game collisions with game assets
"""
import pyxel


class Collision:
    """ Collision manager class detects players position with save colliders """

    def __init__(self, objects: list = None):
        self.objects = objects if objects else []
        self.player_h = 23 - 7

    def add_collider(self, name: str, **kwargs):
        """
        Adds colliders to self.objects to detect player collision with object during runtime
        :param name: object name
        :param kwargs: object with x,y position plus width and height
        """
        x, y, w, h = kwargs['x'], kwargs['y'], kwargs['w'], kwargs['h']
        self.objects.append({'x1': x, 'y1': y, 'x2': x + w, 'y2': y + h, 'name': name})

    @staticmethod
    def mouse_over_menu(menu_btn: dict):
        """
        Check if mouse current x,y point falls within the buttons rectangle
        :param menu_btn: menu Asset class value
        :return: True if within the button else False
        """
        x, y = pyxel.mouse_x, pyxel.mouse_y
        bl = menu_btn['x'], menu_btn['y']
        tr = menu_btn['x'] + menu_btn['w'], menu_btn['y'] + menu_btn['h']
        return bl[0] < x < tr[0] and bl[1] < y < tr[1]

    @staticmethod
    def _check_x(player: dict, obj: dict) -> bool:
        return (obj['x1'] >= player['x2']) or (obj['x2'] <= player['x1'])

    def _check_y(self, player: dict, obj: dict) -> bool:
        return (obj['y2'] <= player['y1'] + self.player_h) or (obj['y1'] >= player['y2'])

    def _check(self, player_coords, obj_coords) -> bool:
        if self._check_x(obj=obj_coords, player=player_coords) or self._check_y(obj=obj_coords, player=player_coords):
            return False
        return True

    def does_player_collide(self, player_x: int, player_y: int, player_w: int, player_h: int) -> bool:
        """
        Checks if player current rectangle position overlaps with any known object rectangle
        :param player_x: players future x position
        :param player_y: players future y position
        :param player_w: players current width
        :param player_h: players current length
        :return: True if player collides with object else False
        """
        player_coords = {'x1': player_x, 'y1': player_y, 'x2': player_x + player_w, 'y2': player_y + player_h}
        for obj in self.objects:
            if self._check(player_coords=player_coords, obj_coords=obj):
                return True
        return False
