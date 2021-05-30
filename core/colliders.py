class Collision:

    def __init__(self, objects: list = None):
        self.objects = objects if objects else []
        self.player_h = 23 - 7

    def add_collider(self, x: int, y: int, w: int, h: int, name: str, *args, **kwargs):
        _, _ = args, kwargs
        self.objects.append({'x1': x, 'y1': y, 'x2': x + w, 'y2': y + h, 'name': name})

    @staticmethod
    def _check_x(p: dict, obj: dict) -> bool:
        return (p['x1'] >= obj['x2']) or (p['x2'] <= obj['x1'])

    def _check_y(self, p: dict, obj: dict) -> bool:
        return (p['y2'] <= obj['y1'] + self.player_h) or (p['y1'] >= obj['y2'])

    def _check(self, player_coords, obj_coords) -> bool:
        if self._check_x(p=obj_coords, obj=player_coords) or self._check_y(p=obj_coords, obj=player_coords):
            return False
        return True

    def does_player_collide(self, player_x: int, player_y: int, player_w: int, player_h: int) -> bool:
        player_coords = {'x1': player_x, 'y1': player_y, 'x2': player_x + player_w, 'y2': player_y + player_h}
        for obj in self.objects:
            if self._check(player_coords=player_coords, obj_coords=obj):
                return True
        return False
