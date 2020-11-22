import pyxel
from collections import deque, namedtuple
from random import randint

Point = namedtuple("Point", ["w", "h"])     # 猫の向き

UP = Point(-16, 16)
DOWN = Point(16, 16)
RIGHT = Point(-16, 16)
LEFT = Point(16, 16)


class App:
    music_flug = False
    def __init__(self):
        pyxel.init(160, 120, caption="Hello Pyxel!")
        pyxel.load("test.pyxres")   # player(48, 16), food(48, 0)
        self.direction = RIGHT

        # Score
        self.score = 0
        self.harts = 5
        
        # Starting Point
        self.player_x = 42
        self.player_y = 60
        self.player_vy = 0
        self.food = [(i * 60, randint(0, 104), True) for i in range(4)]
        self.enemy = [(i * 60, randint(0, 104), True) for i in range(4)]

        pyxel.run(self.update, self.draw)
        

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.update_player

        for i, v in enumerate(self.food):
            self.food[i] = self.update_food(*v)

        for i, v in enumerate(self.enemy):
            self.enemy[i] = self.update_enemy(*v)

        self.update_player()
        
        # bgm
        if self.music_flug == False:
            pyxel.playm(0, loop=True)
            self.music_flug = True

    def update_player(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x = max(self.player_x - 2, 0)
            self.direction = LEFT

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x = min(self.player_x + 2, pyxel.width - 16)
            self.direction = RIGHT

        if pyxel.btn(pyxel.KEY_UP):
            self.player_y = max(self.player_y - 2, 0)
            self.direction = UP

        if pyxel.btn(pyxel.KEY_DOWN):
            if self.player_y != 104:
                self.player_y = min(self.player_y + 2, pyxel.width - 16)
                self.direction = DOWN

    def draw(self):
        # bg color
        #pyxel.cls(6)

        # tile map
        pyxel.bltm(0, 0, 0, 0, 0, 20, 15, 0)

        # draw food
        for x, y, is_active in self.food:
            if is_active:
                pyxel.blt(x, y, 0, 48, 0, 16, 16, 0)

        # draw enemy
        for x, y, is_active in self.enemy:
            if is_active:
                pyxel.blt(x, y, 0, 48, 32, -16, 16, 0)

        # draw cat
        pyxel.blt(
            self.player_x, 
            self.player_y, 
            0, 
            48 if self.player_vy > 48 else 48, 
            16, 
            self.direction[0], 
            self.direction[1], 
            0
        )

        # print score
        s = "Score {:>4}".format(self.score)
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)

        # draw hart
        self.draw_harts()
        

    def update_food(self, x, y, is_active):
        if is_active and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:   # abs関数は絶対値を返す
            is_active = False
            self.score += 100
            self.player_vy = min(self.player_vy, -8)
            pyxel.play(3, 4)

            # se
            pyxel.play(2, 10, loop=False)

        x -= 2

        if x < -40:
            x += 240
            y = randint(0, 104)
            is_active = True

        return (x, y, is_active)

    def update_enemy(self, x, y, is_active):
        if is_active and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:   # abs関数は絶対値を返す
            is_active = False
            self.player_vy = min(self.player_vy, -8)
            pyxel.play(3, 4)
            self.harts -= 1

            # se
            pyxel.play(2, 11, loop=False)

        x += 2

        if x > 160:
            x = -16
            y = randint(0, 104)
            is_active = True

        return (x, y, is_active)
    
    def draw_harts(self):
        if self.harts == 5:
            dhart = 80
        elif self.harts == 4:
            dhart = 64
        elif self.harts == 3:
            dhart = 48
        elif self.harts == 2:
            dhart = 32
        elif self.harts == 1:
            dhart = 16
        else:
            dhart = 0

        pyxel.blt(80, 0, 0, 48, 96, dhart, 16, 0)
        
App()