import pyxel
import json
from player import Player
from door import Door
from key import Key
from button import Button
from rooms import Room

class App:
    def __init__(self):
        self.gamestate = 0
        self.player = Player(0, 0, 0)
        self.current_screen = 0
        self.offset_x = 0
        self.load_mask('mask.json')
        self.doors = []
        self.rooms = []
        self.keys = [Key(104, 80, 0, 0), Key(56, 112, 1, 0), Key(56, 88, 1, 2), Key(120, 112, 2, 0)]
        self.buttons = [Button(56, 32, 0), Button(64, 64, 1), Button(48, 48, 2), Button(72, 80, 2)]

        pyxel.init(128, 128, title='SpaceWarp')
        pyxel.load("assets/1.pyxres")
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

        if self.player.deaded == 1:
            self.gamestate = 0
            return

        self.player.move()
        self.process_key_interaction()
        self.process_button_interaction()
        self.update_door_status()
        self.update_screen_position()

    def process_key_interaction(self):
        player_key = self.player.OnKey(self.keys, self.current_screen)
        if player_key == -1:
            return

        for key in self.keys:
            if key.col == player_key and key.screen == self.current_screen:
                key.active = False
                for door in self.doors:
                    if door.col == key.col and door.screen == self.current_screen:
                        door.opening = 1

    def process_button_interaction(self):
        for button in self.buttons:
            button.update_button()
            for door in self.doors:
                if (
                    button.screen == self.current_screen
                    and door.screen == self.current_screen
                    and door.col == 1
                ):
                    if button.active_time != 0:
                        door.opening = 1
                    else:
                        door.opening = 0

    def update_door_status(self):
        for door in self.doors:
            if door.opening == 1 and door.active != 0:
                door.active -= 1
            elif door.opening == 0 and door.active != 8:
                door.active += 1

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
            
            for i in self.doors:
                i.draw_door(self.current_screen)
                
            for i in self.keys:
                i.draw_key(self.current_screen)
                
            for i in self.buttons:
                i.draw_button(self.current_screen)
                
            self.player.draw_player()

App()