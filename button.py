import pyxel

class Button:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.active_time = 0

    def update_button(self):
        if self.active_time > 0:
            self.active_time -= 1

    def draw_button(self, screen):
        if screen == self.screen:
            pyxel.blt(self.x, self.y, 0, 16, 32, 8, 8, 0)