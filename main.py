import pyxel, json, copy, math
from player import Player
from rooms import Room
from menu import Menu

def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier

class App:
    def __init__(self):
        self.gamestate = 0
        self.player = Player(0, 112, 0)
        self.current_screen = 0
        self.menu = Menu()

        pyxel.init(128, 128, title='SpaceWarp')
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
                self.start_frame = pyxel.frame_count
                self.end_frame = 0
            return
        if self.gamestate == 2:
            return
        self.player.move(self.rooms[self.current_screen], self.current_screen, self.difficulty)
        self.update_screen_position()
        self.rooms[self.current_screen].update_room(self.player.x, self.player.y)
        
        if self.player.alive == 0 or pyxel.btnr(pyxel.KEY_R):
            self.player.reset(self.rooms[self.current_screen].spawn_x, self.rooms[self.current_screen].spawn_y)
            self.player.alive = 1
            self.rooms[self.current_screen] = copy.deepcopy(self.enter_room_state)
        
        if self.player.win == 1:
            self.gamestate = 2
            self.end_frame = pyxel.frame_count
            self.total_time = str(round_half_up((self.end_frame - self.start_frame)/30, 2))
            self.end_anim_frame = 0

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
        if self.menu.debug == 1:
            debug_prefix = " (DEBUG)"
        else:
            debug_prefix = ""

        if self.gamestate == 0:
            pyxel.cls(0)
            self.menu.draw_menu()
            pyxel.title("SpaceWarp" + debug_prefix)
        elif self.gamestate == 1:
            pyxel.cls(0)
            pyxel.bltm(0, 0, self.difficulty + 1, self.current_screen * 128, 0, 128, 128)
            self.rooms[self.current_screen].draw_room()
            self.player.draw_player()

            if self.menu.debug == 1 and (pyxel.btnp(pyxel.KEY_LEFTBRACKET) or pyxel.btnp(pyxel.KEY_RIGHTBRACKET)):
                if pyxel.btnp(pyxel.KEY_LEFTBRACKET):
                    self.current_screen = (self.current_screen - 1) % len(self.rooms)
                if pyxel.btnp(pyxel.KEY_RIGHTBRACKET):
                    self.current_screen = (self.current_screen + 1) % len(self.rooms)

                if self.current_screen == 1 or self.current_screen == 3:
                    self.rooms[self.current_screen].spawn_x = 0
                    self.rooms[self.current_screen].spawn_y = 112
                elif self.current_screen == 2:
                    self.rooms[self.current_screen].spawn_x = 0
                    self.rooms[self.current_screen].spawn_y = 48

                self.enter_room_state = copy.deepcopy(self.rooms[self.current_screen])
                self.player.alive = 0

            if debug_prefix != "":
                pyxel.title("SpaceWarp" + debug_prefix + f" | Difficulty: {self.difficulty} | Current Screen: {self.current_screen} | Player Position: ({self.player.x}, {self.player.y}) | Room Spawn: ({self.rooms[self.current_screen].spawn_x}, {self.rooms[self.current_screen].spawn_y})")
            else: 
                pyxel.title("SpaceWarp")
        elif self.gamestate == 2:
            pyxel.title("SpaceWarp" + debug_prefix)
            pyxel.cls(0)
            if self.end_anim_frame < 72:
                pyxel.bltm(0, 0, 0, 128, 0, 128, 64)
                pyxel.blt(88, 48 - self.end_anim_frame, 0, 0, 64, 16, 24)  
                pyxel.bltm(0, 64, 0, 128, 64, 128, 64)
                self.end_anim_frame += 1        
            else:
                pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
                pyxel.text(48, 48, "You win!", 7)
                pyxel.text(40, 56, "Time: " + self.total_time + "s", 7)
                pyxel.text(42, 72, "Difficulty:", 7)
                pyxel.text(48, 80, str(self.menu.options[1][self.difficulty]), 0)

App()