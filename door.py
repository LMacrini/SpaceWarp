import pyxel

class Door:
    def __init__(self, x, y, screen, col):
        self.x = x
        self.y = y
        self.screen = screen
        self.col = col
        self.active = 8
        self.opening = 0

    def draw_door(self, current_screen):
        if self.screen == current_screen:
            pyxel.blt(self.x, self.y, 0, 32 + 8 * self.col, 40 - self.active, 8, self.active, 0)
            pyxel.blt(self.x, self.y + 16 - self.active, 0, 32 + 8 * self.col, 40, 8, self.active, 0)