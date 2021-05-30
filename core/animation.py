"""animation.py
This module holds the classes required to manage game animations
"""
from itertools import cycle
from random import randint
from core.asset_manager import Assets


class Animation:
    """ Animation manager class to help determine next animation frame during gameplay """

    def __init__(self):
        # idle frame
        self.idling = [Assets.IDLE_0, Assets.IDLE_1, Assets.IDLE_2, Assets.IDLE_1]

        # setup walk animations
        self.walk_left_frame = [Assets.WALK_LEFT_1, Assets.WALK_LEFT_2]
        self.walk_right_frame = [Assets.WALK_RIGHT_1, Assets.WALK_RIGHT_2]
        self.walk_up_frame = [Assets.WALK_UP_1, Assets.WALK_UP_2]
        self.walk_down_frame = [Assets.WALK_DOWN_1, Assets.WALK_DOWN_2]

        # cycle between index 0 and 1 for idle frames and keep track of last index
        self.idle_frame_index = [cycle(sorted([0, 1, 2, 3] * 4)), 0]

        # cycle between index 0 and 1 for walk frames
        self.walk_frame_index = cycle(sorted([0, 1] * 3))

    def get_idle_animation(self) -> dict:
        """
        :return: return the correct idle frame with random idling based on randint range output and last index
        """
        if self.idle_frame_index[1] == 0 and randint(0, 100) < 90:
            return self.idling[self.idle_frame_index[1]]
        self.idle_frame_index[1] = next(self.idle_frame_index[0])
        return self.idling[self.idle_frame_index[1]]

    def get_walk_animation(self, direction: int) -> dict:
        """
        :param direction: -1:idle, 0:left, 1:right, 2:up, 3:down
        :return: return the correct walk animation frame
        """
        if direction == 0:
            return self.walk_left_frame[next(self.walk_frame_index)]
        if direction == 1:
            return self.walk_right_frame[next(self.walk_frame_index)]
        if direction == 2:
            return self.walk_up_frame[next(self.walk_frame_index)]
        if direction == 3:
            return self.walk_down_frame[next(self.walk_frame_index)]
        return self.get_idle_animation()
