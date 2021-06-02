import pyxel


class Menu:

    def __init__(self):
        self.sounds = {
            'play': {'ch': 0, 'snd': 0, 'loop': False},
            'reset': {'ch': 0, 'snd': 0, 'loop': False},
            'quit': {'ch': 0, 'snd': 0, 'loop': False},
        }

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

    def play(self, sound: str):
        pyxel.play(**self.sounds[sound])
