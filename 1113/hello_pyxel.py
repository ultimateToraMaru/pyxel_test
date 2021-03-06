import pyxel
import time
from collections import deque, namedtuple
from random import randint
from enum import Enum, auto                 # enumを使ってゲームシーンを管理

Point = namedtuple("Point", ["w", "h"])     # 猫の向き

UP = Point(-16, 16)
DOWN = Point(16, 16)
RIGHT = Point(-16, 16)
LEFT = Point(16, 16)

class GAMESCENE(Enum):
    # 画面のシーンをEnumで定義する
    Title = auto()
    Main = auto()
    GameOver = auto()

class App:
    music_flag = False
    item_sw = False
    def __init__(self):
        pyxel.init(160, 120, caption="Hello Pyxel!")    # pixel(160, 120) tilemap(20, 15)
        self.game_scene = GAMESCENE.Title
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
        self.enemy2 = [(i * 60, randint(0, 104), False) for i in range(4)]
        self.item = [(i * 60, randint(0, 104), False) for i in range(1)]

        self.logo_x = 0
        self.logo_y = -32

        self.start = 0
        self.speed = 1

        pyxel.run(self.update, self.draw)
        
    def update(self):
        if self.game_scene == GAMESCENE.Title:
            self.update_title()
        elif self.game_scene == GAMESCENE.Main:
            self.update_main()
        elif self.game_scene == GAMESCENE.GameOver:
            self.update_gameover()

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
        # pyxel.cls(6)

        pyxel.cls(0) # 一旦画面を真っ新にする
        if self.game_scene == GAMESCENE.Title:
            self.draw_title()

        elif self.game_scene == GAMESCENE.Main:
            self.draw_main()

        elif self.game_scene == GAMESCENE.GameOver:
            self.draw_gameover()

    def update_food(self, x, y, is_active):
        if is_active and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:   # abs関数は絶対値を返す
            is_active = False
            self.score += 100
            self.player_vy = min(self.player_vy, -8)
            pyxel.play(3, 4)

            # se
            pyxel.play(2, 10, loop=False)

            if(self.score != 0 and self.score % 1000 == 0):
                print('speed up')
                self.speed += 0.5

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

            if(self.item_sw == False):
                self.harts -= 1
                pyxel.play(2, 11, loop=False)
                
            else:
                self.score += 200
                pyxel.play(2, 10, loop=False)
                if(time.time() > self.start + 5):
                    self.item_sw = False
            
        x += self.speed

        if x > 160:
            x = -16
            y = randint(0, 104)
            is_active = True

        return (x, y, is_active)

    def update_enemy2(self, x, y, is_active):
        if is_active and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:   # abs関数は絶対値を返す
            is_active = False
            self.player_vy = min(self.player_vy, -8)
            pyxel.play(3, 4)
            self.harts -= 1

            # se
            pyxel.play(2, 11, loop=False)

        y += 1

        if y > 200:
            x = randint(0, 104)
            y = 0
            is_active = True

        return (x, y, is_active)

    def update_item(self, x, y, is_active):
        if is_active and abs(x - self.player_x) < 12 and abs(y - self.player_y) < 12:   # abs関数は絶対値を返す
            is_active = False
            self.score += 300
            self.player_vy = min(self.player_vy, -8)
            pyxel.play(3, 4)
            self.item_sw = True
            self.start = time.time()
            self.harts += 1
            # bgm
            pyxel.stop(0)
            pyxel.play(0, 2, loop=True)

            self.music_flag = False

            # se
            pyxel.play(2, 12, loop=False)

        y += 2

        if y > 1000:
            x = randint(0, 104)
            y = 0
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
    
    def update_title(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.game_scene = GAMESCENE.Main

    def update_main(self):
        if self.harts == 0:
            self.game_scene = GAMESCENE.GameOver

        self.update_player

        for i, v in enumerate(self.food):
            self.food[i] = self.update_food(*v)

        for i, v in enumerate(self.enemy):
            self.enemy[i] = self.update_enemy(*v)

        if(self.score > 2000):
            for i, v in enumerate(self.enemy2):
                self.enemy2[i] = self.update_enemy2(*v)

        for i, v in enumerate(self.item):
            self.item[i] = self.update_item(*v)

        self.update_player()
        
        # bgm
        if (self.music_flag == False and self.item_sw == False):
            pyxel.stop(0)
            pyxel.playm(0, loop=True)
            self.music_flag = True

        # if (self.item_sw == True):


        # elif (self.item_sw == False):
        #     pyxel.stop(0)
        #     pyxel.playm(0, loop=True)
        
        # print('music_flag: ' ,)
        # print(self.music_flag)
        # print('item_flag: ' ,)
        # print(self.item_sw)

    def update_gameover(self):
        if pyxel.btnp(pyxel.KEY_SPACE):
            pyxel.quit()

    def draw_title(self):
        pyxel.cls(6)
        pyxel.text(44, 100, "Press Space Key !", 0)
        pyxel.blt(self.logo_x, self.logo_y, 1, 0, 0, 160, 32, 2)
        if(self.logo_y < 32):
            self.update_logo()

    def draw_main(self):
        # tile map
        pyxel.bltm(0, 0, 0, 0, 0, 20, 15, 0)

        # draw food
        for x, y, is_active in self.food:
            if is_active:
                pyxel.blt(x, y, 0, 48, 0, 16, 16, 0)

        # draw enemy
        for x, y, is_active in self.enemy:
            if is_active:
                if(self.item_sw == False):
                    pyxel.blt(x, y, 0, 48, 32, -16, 16, 0)
                else:
                    pyxel.blt(x, y, 0, 64, 32, -16, 16, 0)

        # draw enemy2
        for x, y, is_active in self.enemy2:
            if is_active:
                pyxel.blt(x, y, 0, 48, 64, 16, 16, 0)

        # draw item
        for x, y, is_active in self.item:
            if is_active:
                pyxel.blt(x, y, 0, 64, 0, 16, 16, 0)

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
        
    def draw_gameover(self):
        # bgmストップ
        pyxel.stop(0)
        pyxel.stop(1)

        # print score
        s = "Score {:>4}".format(self.score)
        pyxel.text(5, 4, s, 1)
        pyxel.text(4, 4, s, 7)

        pyxel.text(75, 0, "game over!", 5)
    
    def update_logo(self):
        self.logo_x = 0
        self.logo_y += 0.5

App()