"""assets.py
This module holds the classes required to manage game assets and tile-map location
"""
from pathlib import Path
import pyxel
from core.colliders import Collision


class Assets(dict):
    """ Map out the tile-map to extract assets at correct pixel coordinates """
    # rooms
    BEDROOM = {'x': 0, 'y': 0, 'img': 0, 'u': 0, 'v': 0, 'w': 100, 'h': 100}
    ROOM = {'x': 0, 'y': 0, 'img': 0, 'u': 0, 'v': 100, 'w': 100, 'h': 100}

    # assets
    BED = {'x': 0, 'y': 52, 'img': 0, 'u': 206, 'v': 0, 'w': 29, 'h': 46, 'colkey': 15}
    COMPUTER = {'x': 3, 'y': 9, 'img': 0, 'u': 169, 'v': 0, 'w': 36, 'h': 32, 'colkey': 15}
    BOOKSHELF = {'x': 72, 'y': 2, 'img': 0, 'u': 142, 'v': 0, 'w': 26, 'h': 33, 'colkey': 15}
    CLOSET = {'x': 80, 'y': 47, 'img': 0, 'u': 122, 'v': 0, 'w': 20, 'h': 50, 'colkey': 15}
    MAT = {'x': 45, 'y': 87, 'img': 0, 'u': 144, 'v': 77, 'w': 13, 'h': 8, 'colkey': 15}
    WINDOW = {'x': 44, 'y': 3, 'img': 0, 'u': 182, 'v': 97, 'w': 23, 'h': 15, 'colkey': 15}

    # character
    IDLE = {'img': 0, 'u': 0, 'v': 234, 'w': 17, 'h': 22, 'colkey': 15}
    SIT = {'img': 0, 'u': 17, 'v': 237, 'w': 17, 'h': 19, 'colkey': 15}
    WALK_DOWN_1 = {'img': 0, 'u': 34, 'v': 234, 'w': 17, 'h': 22, 'colkey': 15}
    WALK_DOWN_2 = {'img': 0, 'u': 51, 'v': 234, 'w': 17, 'h': 22, 'colkey': 15}
    WALK_UP_1 = {'img': 0, 'u': 68, 'v': 234, 'w': 17, 'h': 22, 'colkey': 15}
    WALK_UP_2 = {'img': 0, 'u': 85, 'v': 234, 'w': 17, 'h': 22, 'colkey': 15}
    WALK_LEFT_1 = {'img': 0, 'u': 102, 'v': 234, 'w': 14, 'h': 22, 'colkey': 15}
    WALK_LEFT_2 = {'img': 0, 'u': 116, 'v': 234, 'w': 14, 'h': 22, 'colkey': 15}
    WALK_RIGHT_1 = {'img': 0, 'u': 130, 'v': 234, 'w': 14, 'h': 22, 'colkey': 15}
    WALK_RIGHT_2 = {'img': 0, 'u': 144, 'v': 234, 'w': 14, 'h': 22, 'colkey': 15}


class AssetManager:
    """ Loads the tile-map coordinates into an image bank as well as manage collisions for the tile """

    def __init__(self, collision: Collision):
        base_dir = Path(__file__).resolve().parent.parent
        asset_pyres = Path.joinpath(base_dir, 'assets/tilemap.pyxres').as_posix()
        pyxel.load(filename=asset_pyres)

        # static objects
        wall = {'x': 0, 'y': 0, 'w': 100, 'h': 23, 'name': 'wall'}

        # add asset colliders
        self.collision = collision
        self.collision.add_collider(**wall)

        # startup colliders
        self.collision.add_collider(**Assets.BED, name='bed')
        self.collision.add_collider(**Assets.COMPUTER, name='computer')
        self.collision.add_collider(**Assets.BOOKSHELF, name='bookshelf')
        self.collision.add_collider(**Assets.CLOSET, name='closet')

    @staticmethod
    def _draw_bedroom():
        pyxel.blt(**Assets.BEDROOM)
        pyxel.blt(**Assets.BED)
        pyxel.blt(**Assets.COMPUTER)
        pyxel.blt(**Assets.BOOKSHELF)
        pyxel.blt(**Assets.CLOSET)
        pyxel.blt(**Assets.MAT)
        pyxel.blt(**Assets.WINDOW)

    @staticmethod
    def _draw_kitchen():
        pyxel.blt(**Assets.ROOM)

    @staticmethod
    def _draw_bathroom():
        pyxel.blt(**Assets.ROOM)

    @staticmethod
    def draw_player(x: int, y: int, frame: dict):
        """
         Pyxel draw players current position using player frame passed
        :param x: players current x position
        :param y: players current y position
        :param frame: players current animation frame
        """
        pyxel.blt(x=x, y=y, **frame)

    def draw_room(self, room: int):
        """
        Pyxel draw the current room player is in.
        :param room: 0:bedroom, 1:kitchen, 2:bathroom
        """
        if room == 0:
            self._draw_bedroom()
        elif room == 1:
            self._draw_kitchen()
        elif room == 2:
            self._draw_bathroom()
