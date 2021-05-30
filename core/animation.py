from itertools import cycle
from core.assets import Assets


class Animation:

    def __init__(self):
        self.idle = Assets.IDLE
        self.walk_left_frame = [Assets.WALK_LEFT_1, Assets.WALK_LEFT_2]
        self.walk_right_frame = [Assets.WALK_RIGHT_1, Assets.WALK_RIGHT_2]
        self.walk_up_frame = [Assets.WALK_UP_1, Assets.WALK_UP_2]
        self.walk_down_frame = [Assets.WALK_DOWN_1, Assets.WALK_DOWN_2]

        self.frame_index = cycle(sorted([0, 1] * 3))

    def get_walk_animation(self, direction: int) -> dict:
        """
        :param direction: 0:left, 1:right, 2:up, 3:down
        :return: return the correct animation
        """
        if direction == 0:
            return self.walk_left_frame[next(self.frame_index)]
        elif direction == 1:
            return self.walk_right_frame[next(self.frame_index)]
        if direction == 2:
            return self.walk_up_frame[next(self.frame_index)]
        elif direction == 3:
            return self.walk_down_frame[next(self.frame_index)]
        else:
            return self.idle
