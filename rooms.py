class Room:
    def __init__(self, objects):
        self.objects = objects
        self.keys = [1] * 3
        self.doors = [0] * 3
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