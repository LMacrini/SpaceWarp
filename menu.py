import pyxel, webbrowser

class Menu:
    def __init__(self):
        self.menu_state = 0
        self.selection = 0
        self.difficulty = 0
        self.deadzone = 2000
        self.controller_over_deadzone = 0
        self.options = [['Start', 'Difficulty', 'Help'],
                        ['Easy', 'Normal', 'Hard', 'Lunatic', 'Back']]
    def update_menu(self):
        if pyxel.btnp(pyxel.KEY_DOWN) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN) or pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY) > self.deadzone:
            if self.controller_over_deadzone == 0:
                self.selection = (self.selection + 1) % len(self.options[self.menu_state])
            self.controller_over_deadzone = -1
        elif pyxel.btnp(pyxel.KEY_UP) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP) or pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY) < -self.deadzone:
            if self.controller_over_deadzone == 0:
                self.selection = (self.selection - 1) % len(self.options[self.menu_state])
            self.controller_over_deadzone = 1
        else:
            self.controller_over_deadzone = 0

        menu_state = self.menu_state
        if pyxel.btnp(pyxel.KEY_RETURN) or pyxel.btnp(pyxel.KEY_Z) or pyxel.btnr(pyxel.GAMEPAD1_BUTTON_A):
            if self.selection == 0 and menu_state == 0:
                return 1
            elif self.selection == 1 and menu_state == 0:
                menu_state = 1
            elif (self.selection == 4 and menu_state == 1
                or self.selection == 0 and menu_state == 2
            ):
                menu_state = 0
            elif self.selection == 2 and menu_state == 0:
                webbrowser.open("https://github.com/Wam25/SpaceWarp")
            elif menu_state == 1:
                self.difficulty = self.selection

        if self.menu_state != menu_state:
            self.menu_state = menu_state
            self.selection = 0

        return 0

    def draw_menu(self):
        pyxel.bltm(0, 0, 0, 0, 0, 128, 128)
        for i, v in enumerate(self.options[self.menu_state]):
            if i == self.selection:
                col = 0
            elif self.menu_state == 1 and i == self.difficulty:
                col = 5
            else:
                col = 7
            
            pyxel.text(42, 8 * (i - ((len(self.options[self.menu_state]) + 1)/2)) + 72, v, col)
