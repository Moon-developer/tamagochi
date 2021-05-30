import pyxel
from core import AssetManager, Animation, Collision


class Tamagotchi:
    def __init__(self):
        # init
        self.screen_w = 100
        self.screen_h = 100
        self.room_w = self.screen_w
        self.room_h = self.screen_h - 22  # minus the room wall height
        pyxel.init(self.screen_w, self.screen_h, caption="Tamagotchi")
        pyxel.mouse(True)
        self.player_x = 0
        self.player_y = 25
        self.player_w = 17
        self.player_h = 22
        self.current_room = 0  # 0 = bedroom, 1 = kitchen, 2 = bathroom
        self.direction = -1

        # load assets
        self.collision = Collision()
        self.assets = AssetManager(collision=self.collision)

        # load animation manager
        self.animation = Animation()

        # run game
        pyxel.run(self.update, self.draw)

    def check_colliders(self, move_x: int = 0, move_y: int = 0) -> bool:
        results = self.collision.does_player_collide(
            player_x=self.player_x + move_x,
            player_y=self.player_y + move_y,
            player_h=self.player_h,
            player_w=self.player_w
        )
        return results

    def move_character(self):
        self.direction = -1
        if pyxel.btn(pyxel.KEY_LEFT):
            if 0 <= self.player_x - 1 <= self.room_w and not self.check_colliders(move_x=-1):
                self.player_x -= 1
                self.direction = 0
        if pyxel.btn(pyxel.KEY_RIGHT):
            if 0 <= self.player_x + 1 <= self.room_w - self.player_w and not self.check_colliders(move_x=1):
                self.player_x += 1
                self.direction = 1
        if pyxel.btn(pyxel.KEY_UP):
            if 0 <= self.player_y - 1 <= self.room_h and not self.check_colliders(move_y=-1):
                self.player_y -= 1
                self.direction = 2
        if pyxel.btn(pyxel.KEY_DOWN):
            if 0 <= self.player_y + 1 <= self.room_h and not self.check_colliders(move_y=1):
                self.player_y += 1
                self.direction = 3

    def change_room(self):
        if pyxel.btnp(pyxel.KEY_1):
            self.current_room = 0
        if pyxel.btnp(pyxel.KEY_2):
            self.current_room = 1
        if pyxel.btnp(pyxel.KEY_3):
            self.current_room = 2

    def update(self):
        self.move_character()
        self.change_room()

        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

    def draw(self):
        # clear screen
        pyxel.cls(0)

        # draw assets in current room
        self.assets.draw_room(room=self.current_room)

        # # draw player
        frame = self.animation.get_walk_animation(direction=self.direction)
        self.assets.draw_player(x=self.player_x, y=self.player_y, frame=frame)
