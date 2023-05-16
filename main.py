from player import Player
from door import Door
from key import Key
from button import Button
from rooms import Room
import pyxel, json


class App:
    def __init__(self):
        self.Gamestate = 0
        self.player = Player(0, 0, 0)
        self.current_screen = 0
        self.max_screen = -1
        self.u = 0

        self.load_mask('mask.json')
        print(self.mask[0].objects)
        self.doors = []
        self.rooms = []
        
        self.keys = [Key(104, 80, 0, 0), Key(56, 112, 1, 0), Key(56, 88, 1, 2), Key(120, 112, 2, 0)]
        self.buttons = [Button(56, 32, 0), Button(64, 64, 1), Button(48, 48, 2), Button(72, 80, 2)]
        pyxel.init(128, 128, title='SpaceWarp')
        pyxel.load("assets/1.pyxres")
        pyxel.run(self.update, self.draw)
        
    def load_mask(self, file_name):
        file = open(file_name, 'r')
        mask = json.loads(file.read())
        self.mask = []
        for i in mask:
            self.mask.append(Room(i))
        file.close()

    def update(self):
        
        if pyxel.btn(pyxel.KEY_S):
            self.Gamestate = 1
            
        if self.Gamestate == 0:
            pass
        else:
            if self.player.deaded == 1:
                self.Gamestate = 0
            else:
                self.player.move()

                self.player.on_key = self.player.OnKey(self.keys, self.current_screen)
                if self.player.on_key != -1:
                    for i in self.keys:
                        if i.col == self.player.on_key and i.screen == self.current_screen:
                            i.active = False
                            for j in self.doors:
                                if j.col == i.col and j.screen == self.current_screen:
                                    j.opening = 1

                self.player.OnButton(self.buttons, self.current_screen)
                for i in self.buttons:
                    i.update_button()
                    for j in self.doors:
                        if i.screen == self.current_screen and j.screen == self.current_screen and j.col == 1:
                            if i.active_time != 0:
                                j.opening = 1
                            else:
                                j.opening = 0

                for i in self.doors:
                    if i.opening == 1 and i.active != 0:
                        i.active -= 1
                    elif i.opening == 0 and i.active != 8:
                        i.active += 1
                
                if self.player.x == 128:
                        self.u += 128
                        self.current_screen += 1
                        self.player.x -= 128
                        self.player.y -= 2
                elif self.player.x == -1 and self.current_screen != 0:
                        self.u -= 128
                        self.current_screen -= 1
                        self.player.x += 128
                        self.player.y -= 2

                pyxel.bltm(0, 0, 2, self.u, 128, 128, 128)

                if self.current_screen > self.max_screen:
                    self.max_screen = self.current_screen
                    self.rooms.append(Room([[pyxel.pget(i*8, j*8)] for j in range(16)] for i in range(16)))

            
    
    def draw(self):
        if self.Gamestate == 0:
            pyxel.cls(0)
            pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
            pyxel.text(42,64, '(S)tart', 7)
        else:
            
            pyxel.cls(0)
            pyxel.bltm(0, 0, 2, self.u, 0, 128, 128)
            for i in self.doors:
                i.draw_door(self.current_screen)
            for i in self.keys:
                i.draw_key(self.current_screen)
            for i in self.buttons:
                i.draw_button(self.current_screen)
            self.player.draw_player()

App()