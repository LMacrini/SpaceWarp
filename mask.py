import pyxel
import json

class App:
    def __init__(self, room_nb, difficulty, path):
        self.room_nb = room_nb
        self.frame_delay = 30
        self.objects = []
        self.types = []
        self.rooms = []
        self.difficulty = difficulty
        self.paths = path
        pyxel.init(128, 128, title='SpaceWarp')
        pyxel.load("ressources/assets.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if 0 < pyxel.frame_count // self.frame_delay <= self.room_nb and pyxel.frame_count % self.frame_delay == 0:
            objects = [[pyxel.pget(x * 8, y * 8) for y in range(16)] for x in range(16)]
            self.objects.append(objects)

        elif self.room_nb < pyxel.frame_count // self.frame_delay <= self.room_nb * 2 and pyxel.frame_count % self.frame_delay == 0:
            types = [[pyxel.pget(x * 8, y * 8) for y in range(16)] for x in range(16)]
            self.types.append(types)
        
        if pyxel.frame_count // self.frame_delay == self.room_nb * 2 and pyxel.frame_count % self.frame_delay == 0:
            self.rooms = [self.room_nb, self.objects, self.types]
            with open(self.paths[self.difficulty], 'w') as file:
                json.dump(self.rooms, file)


        elif pyxel.frame_count // self.frame_delay == self.room_nb * 2 + 1:
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        if 0 <= pyxel.frame_count // self.frame_delay < self.room_nb:
            pyxel.bltm(0, 0, self.difficulty + 1, 128 * (pyxel.frame_count // self.frame_delay), 128, 128, 128)
        elif self.room_nb <= pyxel.frame_count // self.frame_delay < self.room_nb * 2:
            pyxel.bltm(0, 0, self.difficulty + 1, 128 * ((pyxel.frame_count - self.room_nb * self.frame_delay) // self.frame_delay), 256, 128, 128)

path = ['ressources/mask_easy.json', 'ressources/mask_normal.json', 'ressources/mask_hard.json', 'ressources/mask_lunatic.json']
combine = int(input("Combine?"))
full_mask = []

if combine == 0:
    App(int(input("Number of rooms?")), int(input("Difficulty?")), path)
else:
    for i in path:
        with open(i, 'r') as file:
            mask = json.load(file)
            full_mask.append(mask)
    
    with open('ressources/mask.json', 'w') as file:
        json.dump(full_mask, file)