import pyxel
import json
import sys

class App:
    def __init__(self, room_nb, difficulty, path):
        self.room_nb = room_nb
        self.frame_delay = 30
        self.objects = []
        self.types = []
        self.rooms = []
        self.difficulty = difficulty
        self.paths = path
        pyxel.init(128 * room_nb, 256, title='SpaceWarp')
        pyxel.load("ressources/assets.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):
        if pyxel.frame_count < 1:
            return
        for i in range(self.room_nb):
            object = [[pyxel.pget(x * 8 + 128 * i, y * 8) for y in range(16)] for x in range(16)]
            self.objects.append(object)
            types = [[pyxel.pget(x * 8 + 128 * i, y * 8 + 128) for y in range(16)] for x in range(16)]
            self.types.append(types)
        
        self.rooms = [self.room_nb, self.objects, self.types]
        with open(self.paths[self.difficulty], 'w') as file:
            json.dump(self.rooms, file)

        pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, self.difficulty + 1, 0, 128, 128 * self.room_nb, 256)

path = ['ressources/mask_easy.json', 'ressources/mask_normal.json', 'ressources/mask_hard.json', 'ressources/mask_lunatic.json']
combine = int(sys.argv[3])
full_mask = []

if combine == 0:
    App(int(sys.argv[1]), int(sys.argv[2]), path)
else:
    for i in path:
        with open(i, 'r') as file:
            mask = json.load(file)
            full_mask.append(mask)
    
    with open('ressources/mask.json', 'w') as file:
        json.dump(full_mask, file)