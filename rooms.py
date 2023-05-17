class Room:
    def __init__(self, objects):
        self.objects = objects
        self.keys = [1] * 3
        self.doors = [1] * 3
        self.doors_state = [8] * 3

    def collision(self, x, y):
        object_on = self.objects[x // 8][y // 8]
        if (
          object_on  == 1
          or (object_on  == 9 and self.doors[0] == 0)
          or (object_on == 10 and self.doors[1] == 0)
          or (object_on == 11 and self.doors[2] == 0)
        ):
            return 1
        elif object_on == 5:
            return 2