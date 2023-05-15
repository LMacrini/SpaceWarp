import pyxel

class Key:
    def __init__(self, x, y, screen, col):
        self.x = x
        self.y = y
        self.screen = screen
        self.col = col
        self.active = True
    
    def draw_key(self, screen):
        if screen == self.screen and self.active == True:
            pyxel.blt(self.x, self.y, 0, 0 + self.col*8, 48, 8, 8, 0)