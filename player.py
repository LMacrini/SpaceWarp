import pyxel

class Player:
    #setting up player pos, direction and jump=false
    def __init__(self, x, y, d):
        # pyxel.load("assets/1.pyxres")
        self.x = x
        self.y = y
        self.dir = d
        self.moving = 0
        self.jumping = 0
        self.int = 0
        self.grav = 2
        self.deaded = 0
        self.on_key = -1

    #movement    
    def move(self):
        if pyxel.btn(pyxel.KEY_RIGHT) and all(pyxel.pget(self.x + 8, self.y + i) != 1 for i in range(8)):
            self.x += 1
            self.dir = 0
            self.moving = 1
        elif pyxel.btn(pyxel.KEY_LEFT) and all(pyxel.pget(self.x - 1, self.y + i) != 1 for i in range(8)):
            self.x -= 1
            self.dir = 1
            self.moving = 1
        
        else:
            self.moving = 0

        if pyxel.btn(pyxel.KEY_SPACE) and any(pyxel.pget(self.x + i, self.y + 8) == 1 for i in range(8)):
            self.jumping = 12
        
        elif all(pyxel.pget(self.x + i, self.y + 8) != 1 for i in range(8)) and self.jumping == 0: #not intersecting anything:
            if all(pyxel.pget(self.x + i, self.y + 9) != 1 for i in range(8)):
                self.y += self.grav
            else:
                self.y += 1
    
        if any(pyxel.pget(self.x + i, self.y - 1) == 1 for i in range(8)):
            self.jumping = 0
        
        if self.jumping > 0:
            self.y -= 2
            self.jumping -= 1

    def OnKey(self, keys, screen):
        for i in keys:
            if (not ( ( (self.x + 8 < i.x) or (self.x > i.x + 8) ) or ( ( self.y + 8 < i.y) or (self.y > i.y + 8) ) )) and i.screen == screen:
                return i.col
            else:
                return -1
        
    def OnButton(self, buttons, screen):
        for i in buttons:
            if self.y == i.y - 3 and any( ((self.x + j == i.x) or (self.x == i.x + j)) for j in range(8) ) and i.screen == screen:
                i.active_time = 300

    
    def draw_player(self):
        if self.jumping > 0:
            pyxel.blt(self.x, self.y, 0, 24, 8*self.dir, 8, 8, 0)
        elif self.moving == 1:
            pyxel.blt(self.x, self.y, 0, 8*(pyxel.frame_count % 2 + 1), 8*self.dir, 8, 8, 0)
        else:
            pyxel.blt(self.x, self.y, 0, 8 + 8*self.dir, 8*self.dir, 8, 8, 0)
