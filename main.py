import pyxel
import json
from player import Player
from rooms import Room

class App:
    def __init__(self):
        self.gamestate = 0
        self.player = Player(0, 48, 0)
        self.current_screen = 0
        self.offset_x = 0
        self.load_mask('ressources/mask.json')
        self.rooms = []
        
        pyxel.init(128, 128, title='SpaceWarp')
        pyxel.load("ressources/assets.pyxres")
        pyxel.run(self.update, self.draw)
        
    def load_mask(self, file_name):
        with open(file_name, 'r') as file:
            mask = json.load(file)
            self.mask = [Room(i) for i in mask]

    def update(self):
        if pyxel.btn(pyxel.KEY_S):
            self.gamestate = 1

        if self.gamestate == 0:
            return

        self.player.move(self.mask[self.current_screen], self.current_screen)
        self.update_screen_position()
        self.mask[self.current_screen].update_room(self.player.x, self.player.y)

    def update_screen_position(self):
        if self.player.x == 128:
            self.offset_x += 128
            self.current_screen += 1
            self.player.x -= 128
            self.player.y -= 2
        elif self.player.x == -1 and self.current_screen != 0:
            self.offset_x -= 128
            self.current_screen -= 1
            self.player.x += 128
            self.player.y -= 2


    def draw(self):
        if self.gamestate == 0:
            pyxel.cls(0)
            pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
            pyxel.text(42, 64, '(S)tart', 7)
        else:
            pyxel.cls(0)
            pyxel.bltm(0, 0, 2, self.offset_x, 0, 128, 128)
            self.mask[self.current_screen].draw_room()
            self.player.draw_player()

App()