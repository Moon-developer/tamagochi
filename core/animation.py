"""animation.py
This module holds the classes required to manage game animations
"""
from itertools import cycle
from core.assets import Assets


class Animation:
    """ Animation manager class to help determine next animation frame during gameplay """

    def __init__(self):
        # idle frame
        self.idle = Assets.IDLE

        # setup walk animations
        self.walk_left_frame = [Assets.WALK_LEFT_1, Assets.WALK_LEFT_2]
        self.walk_right_frame = [Assets.WALK_RIGHT_1, Assets.WALK_RIGHT_2]
        self.walk_up_frame = [Assets.WALK_UP_1, Assets.WALK_UP_2]
        self.walk_down_frame = [Assets.WALK_DOWN_1, Assets.WALK_DOWN_2]

        # cycle between index 0 and 1 for walk frames
        self.frame_index = cycle(sorted([0, 1] * 3))

    def get_idle_animation(self) -> dict:
        """
        TODO: create multiple idle animations
        :return: return the correct idle animation frame
        """
        return self.idle

    def get_walk_animation(self, direction: int) -> dict:
        """
        :param direction: 0:left, 1:right, 2:up, 3:down
        :return: return the correct walk animation frame
        """
        if direction == 0:
            return self.walk_left_frame[next(self.frame_index)]
        if direction == 1:
            return self.walk_right_frame[next(self.frame_index)]
        if direction == 2:
            return self.walk_up_frame[next(self.frame_index)]
        if direction == 3:
            return self.walk_down_frame[next(self.frame_index)]
        return self.idle
