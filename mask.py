import pyxel
import json

class App:
    def __init__(self, room_nb):
        self.room_nb = room_nb
        self.rooms = []
        pyxel.init(128, 128, title='SpaceWarp')
        pyxel.load("ressources/assets.pyxres")
        pyxel.run(self.update, self.draw)

    def update(self):

        if 0 < pyxel.frame_count <= self.room_nb:
            room = [[pyxel.pget(x * 8, y * 8) for y in range(16)] for x in range(16)]
            self.rooms.append(room)

        if pyxel.frame_count == self.room_nb:
            with open('ressources/mask.json', 'w') as file:
                    json.dump(self.rooms, file)


        elif pyxel.frame_count == self.room_nb + 1:
            pyxel.quit()

    def draw(self):
        pyxel.cls(0)
        pyxel.bltm(0, 0, 2, 128 * (pyxel.frame_count), 128, 128, 128)

App(int(input("Number of rooms?")))
