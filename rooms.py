import pyxel

class Room:
    def __init__(self, objects, types):
        self.objects = objects
        self.types = types
        self.keys = [1] * 3
        self.doors = [1] * 3
        self.doors_state = [8] * 3
        self.button_state = [0] * 3
        self.spawn_x = 0
        self.spawn_y = 0

    def collision(self, x, y):
        if x // 8 > 15 or y // 8 > 15:
            return 0
        
        object_on = self.objects[x // 8][y // 8]
        type_on = self.types[x // 8][y // 8]
        object_below = self.objects[x // 8][y // 8 - 1]
        type_below = self.types[x // 8][y // 8 - 1]
        if (
          object_on  == 1
        or (object_on == 2 and (
            self.doors[type_on - 1] == 1
        ))
        or (object_below == 2 and (
            self.doors[type_below - 1] == 1
        ))
        
        ):
            return 1
        elif 1 < object_on < 7:
            return object_on
        else:
            return 0
    
    def update_room(self, player_x, player_y):
        for i in range(3):
            if self.button_state[i] != 0:
                self.button_state[i] -= 1
        
        for x, a1 in enumerate(self.objects):
            for y, a2 in enumerate(a1):
                type = self.types[x][y]
                if a2 == 2:
                    if self.keys[type - 1] == 0 or self.button_state[type - 1] != 0:
                        self.doors[type - 1] = 0
                    else:
                        self.doors[type - 1] = 1   
                elif a2 == 3:
                    if ( not (player_x + 7 < x * 8 or x * 8 + 7 < player_x
                        or player_y + 7 < y * 8 or y * 8 + 7 < player_y) ):
                        self.keys[type - 1] = 0 
                elif a2 == 4:
                    if x * 8 - 4 <= player_x <= x * 8 + 4 and y * 8 == player_y:
                        self.button_state[type - 1] = 150
                    elif x * 8 - 5 <= player_x <= x * 8 + 5 and y * 8 - 1 <= player_y <= y * 8 and self.button_state[type - 1] <= 2:
                        self.button_state[type - 1] = 2
                    elif x * 8 - 6 <= player_x <= x * 8 + 6 and y * 8 - 2 < player_y <= y * 8 and self.button_state[type - 1] <= 1:
                        self.button_state[type - 1] = 1

        for i in range(3):
            if self.doors[i] == 0 and self.doors_state[i] > 0:
                self.doors_state[i] -= 1
            elif self.doors[i] == 1 and self.doors_state[i] < 8:
                    self.doors_state[i] += 1

    def draw_room(self):
        for x, a1 in enumerate(self.objects):
            for y, a2 in enumerate(a1):
                type = self.types[x][y]
                if a2 == 2:
                    pyxel.blt(x * 8, y * 8, 0, 32 + 8 * (type - 1), 40 - self.doors_state[type - 1], 8, self.doors_state[type - 1], 0)
                    pyxel.blt(x * 8, y * 8 + 16 - self.doors_state[type - 1], 0, 32 + 8 * (type - 1), 40, 8, self.doors_state[type - 1], 0)
                elif a2 == 3 and self.keys[type - 1] == 1:
                    pyxel.blt(x * 8, y * 8, 0, 56, 32 + 8 * (type - 1), 8, 8, 0)
                elif a2 == 4:
                    sprite_x = 4 * ((type-1)**2) - 12 * (type - 1) + 24
                    sprite_y = 8 * ((type-1)**2) - 16 * (type - 1) + 40
                    if self.button_state[type - 1] == 0:
                        pyxel.blt(x * 8, y * 8, 0, sprite_x, sprite_y, 8, 8, 0)
                    elif self.button_state[type - 1] == 1:
                        pyxel.blt(x * 8, y * 8 + 1, 0, sprite_x, sprite_y, 8, 7, 0)
                    elif self.button_state[type - 1] == 2:
                        pyxel.blt(x * 8, y * 8 + 2, 0, sprite_x, sprite_y, 8, 6, 0)