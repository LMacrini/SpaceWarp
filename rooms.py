import pyxel

class Room:
    def __init__(self, objects):
        self.objects = objects
        self.keys = [1] * 3
        self.doors = [1] * 3
        self.doors_state = [8] * 3

    def collision(self, x, y):
        if x // 8 > 15 or y // 8 > 15:
            return 0
        
        object_on = self.objects[x // 8][y // 8]
        if (
          object_on  == 1
          or (self.doors[0] == 1 and (object_on == 9 or self.objects[x // 8][y // 8 - 1] == 9))
          or (self.doors[1] == 1 and (object_on == 10 or self.objects[x // 8][y // 8 - 1] == 10))
          or (self.doors[2] == 1 and (object_on == 11 or self.objects[x // 8][y // 8 - 1] == 11))
        ):
            return 1
        elif 1 < object_on < 7:
            return object_on
        else:
            return 0
    
    def draw_room(self, player_x, player_y):
        for x, a1 in enumerate(self.objects):
            for y, a2 in enumerate(a1):
                if 1 < a2 < 5 and self.keys[a2 - 2] == 1:
                    pyxel.blt(x * 8, y * 8, 0, 56, 32 + 8 * (a2 - 2), 8, 8, 0)
                elif 8 < a2 < 12:
                    pyxel.blt(x * 8, y * 8, 0, 32 + 8 * (a2 - 9), 40 - self.doors_state[a2 - 9], 8, self.doors_state[a2 - 9], 0)
                    pyxel.blt(x * 8, y * 8 + 16 - self.doors_state[a2 - 9], 0, 32 + 8 * (a2 - 9), 40, 8, self.doors_state[a2 - 9], 0)
                elif a2 == 12:
                    if x * 8 - 4 <= player_x <= x * 8 + 4 and y * 8 == player_y:
                        pass
                    elif x * 8 - 5 <= player_x <= x * 8 + 5 and y * 8 - 1 <= player_y <= y * 8:
                        pyxel.blt(x * 8, y * 8 + 2, 0, 16, 32, 8, 6, 0)
                    elif x * 8 - 6 <= player_x <= x * 8 + 6 and y * 8 - 2 < player_y <= y * 8:
                        pyxel.blt(x * 8, y * 8 + 1, 0, 16, 32, 8, 7, 0)
                    else:
                        pyxel.blt(x * 8, y * 8, 0, 16, 32, 8, 8, 0)