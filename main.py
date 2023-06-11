import pyxel
import json
import copy
from player import Player
from rooms import Room
from menu import Menu

class App:

    def __init__(self):
        self.gamestate = 0
        self.player = Player(0, 112, 0)
        self.current_screen = 0
        self.menu = Menu()

        pyxel.init(128, 128, title='SpaceWarp')
        pyxel.icon([
            "00000000000001000000000000000000",
            "00000000010101000000000001010000",
            "00000000000001000010100001010000",
            "00000000000001000010100000000000",
            "00000000000000000001010000000000",
            "00000000000000000001010010100000",
            "00000000101010000000000010100000",
            "00000000000010000000000000000000"
        ], 16)
        pyxel.load("ressources/assets.pyxres")
        pyxel.run(self.update, self.draw)

    def load_mask(self, file_name):
        with open(file_name, 'r') as file:
            mask = json.load(file)
            self.rooms = []
            for i in range(mask[self.difficulty][0]):
                self.rooms.append(Room(mask[self.difficulty][1][i], mask[self.difficulty][2][i]))

    def update(self):
        if self.gamestate == 0:
            self.gamestate = self.menu.update_menu()
            if self.gamestate == 1:
                self.difficulty = self.menu.difficulty
                self.load_mask('ressources/mask.json')
                self.rooms[0].spawn_x, self.rooms[0].spawn_y = 0, 112
                self.enter_room_state = copy.deepcopy(self.rooms[0])
            return

        self.player.move(self.rooms[self.current_screen], self.current_screen, self.difficulty)
        self.update_screen_position()
        self.rooms[self.current_screen].update_room(self.player.x, self.player.y)

        if self.player.alive == 0 or pyxel.btnr(pyxel.KEY_R):
            self.player.reset(self.rooms[self.current_screen].spawn_x, self.rooms[self.current_screen].spawn_y)
            self.player.alive = 1
            self.rooms[self.current_screen] = copy.deepcopy(self.enter_room_state)

    def update_screen_position(self):
        if self.player.x == 124:
            self.current_screen += 1
            self.player.x -= 128
            self.rooms[self.current_screen].spawn_x = self.player.x + 4
            self.rooms[self.current_screen].spawn_y = self.player.y
            self.enter_room_state = copy.deepcopy(self.rooms[self.current_screen])
        elif self.player.x == -5 and self.current_screen != 0:
            self.current_screen -= 1
            self.player.x += 128
            self.rooms[self.current_screen].spawn_x = self.player.x - 4
            self.rooms[self.current_screen].spawn_y = self.player.y
            self.enter_room_state = copy.deepcopy(self.rooms[self.current_screen])

    def draw(self):
        # Clear the screen
        pyxel.cls(0)

        # If the gamestate is 0, draw the menu
        if self.gamestate == 0:
            self.menu.draw_menu()
        else:
            if self.menu.debug == 1 and (pyxel.btnp(pyxel.KEY_LEFTBRACKET) or pyxel.btnp(pyxel.KEY_RIGHTBRACKET)):
                if pyxel.btnp(pyxel.KEY_LEFTBRACKET): self.current_screen = (self.current_screen - 1) % len(self.rooms)
                if pyxel.btnp(pyxel.KEY_RIGHTBRACKET): self.current_screen = (self.current_screen + 1) % len(self.rooms)

                if (self.current_screen == 1 or self.current_screen == 3):
                    self.rooms[self.current_screen].spawn_x = 0
                    self.rooms[self.current_screen].spawn_y = 112
                elif (self.current_screen == 2):
                    self.rooms[self.current_screen].spawn_x = 0
                    self.rooms[self.current_screen].spawn_y = 48

                self.enter_room_state = copy.deepcopy(self.rooms[self.current_screen])

                self.player.alive = 0

            if (self.player.ending == 1):
                self.player.ending = 0
                self.gamestate = 0
                self.player = Player(0, 112, 0)
                self.current_screen = 0
                self.menu.draw_menu()

                if (self.menu.debug == 1): pyxel.title("SpaceWarp (DEBUG)")
                else: pyxel.title("SpaceWarp")

            # Draw the current room and player
            pyxel.bltm(0, 0, self.difficulty + 1, self.current_screen * 128, 0, 128, 128)
            self.rooms[self.current_screen].draw_room()
            self.player.draw_player()

            # Draw debug info
            if (self.menu.debug == 1 and not self.gamestate == 0): pyxel.title(f"SpaceWarp (DEBUG) | Difficulty: {self.difficulty} | Current Screen: {self.current_screen} | Player Position: ({self.player.x}, {self.player.y}) | Room Spawn: ({self.rooms[self.current_screen].spawn_x}, {self.rooms[self.current_screen].spawn_y})")

App()