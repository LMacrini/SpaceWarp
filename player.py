import pyxel

class Player:
    def __init__(self, x, y, d):
        self.x = x
        self.y = y
        self.dir = d
        self.moving = False
        self.jumping = False
        self.gravity = 2
        self.deaded = False
        self.on_key = -1

    def reset_position(self):
        self.x = 0
        self.y = 0
        self.deaded = 0

    def move(self):
        if pyxel.btn(pyxel.KEY_RIGHT) and all(pyxel.pget(self.x + 8, self.y + i) != 1 for i in range(8)):
            self.x += 1
            self.dir = 0
            self.moving = True
        elif pyxel.btn(pyxel.KEY_LEFT) and all(pyxel.pget(self.x - 1, self.y + i) != 1 for i in range(8)):
            self.x -= 1
            self.dir = 1
            self.moving = True
        else:
            self.moving = False

        if pyxel.btn(pyxel.KEY_SPACE) and any(pyxel.pget(self.x + i, self.y + 8) == 1 for i in range(8)):
            self.jumping = True

        elif all(pyxel.pget(self.x + i, self.y + 8) != 1 for i in range(8)) and not self.jumping:
            if all(pyxel.pget(self.x + i, self.y + 9) != 1 for i in range(8)):
                self.y += self.gravity
            else:
                self.y += 1

        if any(pyxel.pget(self.x + i, self.y - 1) == 1 for i in range(8)):
            self.jumping = False

        if self.jumping:
            self.y -= 2

    def OnKey(self, keys, screen):
        for i in keys:
            if self.x + 8 >= i.x and self.x <= i.x + 8 and self.y + 8 >= i.y and self.y <= i.y + 8 and i.screen == screen:
                return i.col
        return -1

    def OnButton(self, buttons, screen):
        for i in buttons:
            if self.y == i.y - 3 and any(self.x + j == i.x or self.x == i.x + j for j in range(8)) and i.screen == screen:
                i.active_time = 300

    def draw_player(self):
        if self.jumping:
            pyxel.blt(self.x, self.y, 0, 24, 8 * self.dir, 8, 8, 0)
        elif self.moving:
            pyxel.blt(self.x, self.y, 0, 8 * (pyxel.frame_count % 2 + 1), 8 * self.dir, 8, 8, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 8 + 8 * self.dir, 8 * self.dir, 8, 8, 0)