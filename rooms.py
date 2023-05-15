class Room:
    def __init__(self, objects):
        self.objects = objects
        self.keys = [1] * 3
        self.doors = [1] * 3
        self.doors_state = [8] * 3