import pyxel
import json

from player import Player
from door import Door
from key import Key
from button import Button
from rooms import Room

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
        with open(file_name, 'r') as file:
            self.mask = [Room(i) for i in json.load(file)]

    def update(self):
        if pyxel.btn(pyxel.KEY_S):
            self.Gamestate = 1

        if self.Gamestate == 0:
            pass
        else:
            if self.player.deaded == 1:
                self.Gamestate = 0
                self.reset_game()  # Reset the game when player dies
            else:
                self.player.move()

                self.update_keys_and_doors()
                self.update_buttons_and_doors()
                self.update_door_states()

                self.handle_screen_transition()

                pyxel.bltm(0, 0, 2, self.u, 128, 128, 128)

                self.check_room_discovery()

                self.check_fire_collision()  # Check for fire collision and kill player if necessary

    def check_fire_collision(self):
        player_tile_x = self.player.x // 8
        player_tile_y = self.player.y // 8

        if (
            self.current_screen < len(self.mask)
            and player_tile_y < len(self.mask[self.current_screen].objects)
            and player_tile_x < len(self.mask[self.current_screen].objects[player_tile_y])
        ):
            room = self.mask[self.current_screen]
            if room.objects[player_tile_x][player_tile_y] == 5:
                self.reset_current_room()
        else:
            self.reset_current_room()

    def reset_current_room(self):
        if self.current_screen < len(self.mask):
            room = self.mask[self.current_screen]
            self.rooms[self.current_screen] = Room(room.objects)
            self.player.reset_position()

    def update_keys_and_doors(self):
        self.player.on_key = self.player.OnKey(self.keys, self.current_screen)
        if self.player.on_key != -1:
            for i in self.keys:
                if i.col == self.player.on_key and i.screen == self.current_screen:
                    i.active = False
                    for j in self.doors:
                        if j.col == i.col and j.screen == self.current_screen:
                            j.opening = 1

    def update_buttons_and_doors(self):
        for i in self.buttons:
            i.update_button()
            for j in self.doors:
                if i.screen == self.current_screen and j.screen == self.current_screen and j.col == 1:
                    j.opening = 1 if i.active_time != 0 else 0

    def update_door_states(self):
        for i in self.doors:
            if i.opening == 1 and i.active != 0:
                i.active -= 1
            elif i.opening == 0 and i.active != 8:
                i.active += 1

    def handle_screen_transition(self):
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

    def check_room_discovery(self):
        if self.current_screen > self.max_screen:
            self.max_screen = self.current_screen
            room = [[pyxel.pget(i * 8, j * 8) for j in range(16)] for i in range(16)]
            self.rooms.append(Room(room))

    def draw(self):
        if self.Gamestate == 0:
            pyxel.cls(0)
            pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
            pyxel.text(42, 64, '(S)tart', 7)
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