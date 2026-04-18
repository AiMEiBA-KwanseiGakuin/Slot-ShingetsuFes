# 自己満足用保存版 made by 金栄智治
import numpy as np
import pygame, sys, os, serial
from pygame.locals import *

WIDTH, HEIGHT = 920, 490+200
Left, Center, Right = 0, 1, 2
Arduino = True#デバック用 Aruinoと接続する場合はTrueに

class MySlot:
    def __init__(self, tile_size = (300, 150), seg_size = (135, 200), game_count = 5):
        self.state = "Wait"
        self.game_count = game_count
        self.tile_num = 21
        self.tile_size = tile_size
        self.seg_size = seg_size
        
        # ↓画像読み込み↓      0      1         2       3        4         5         6
        self.image_name = ["bar", "bell", "cerry", "juggler", "mascat", "replay", "seven"]
        self.images = [pygame.image.load(os.path.join(os.getcwd(), "pictures", name+".jpeg")).convert_alpha() for name in self.image_name]
        self.images = [pygame.transform.scale(image, (self.tile_size)) for image in self.images]
        self.image_num = [pygame.image.load(os.path.join(os.getcwd(), "pictures", str(num)+".jpg")).convert_alpha() for num in range(10)]#7セグ用
        self.image_num = [pygame.transform.scale(image, self.seg_size) for image in self.image_num]#7セグ用
        
        # ↓image_nameと対応する画像の順番↓
        self.left = [4, 5, 4, 0, 2, 4, 5, 4, 3, 6, 4, 5, 4, 2, 0, 4, 5, 4, 5, 6, 1]
        self.center=[3, 2, 4, 0, 5, 2, 4, 1, 5, 2, 4, 0, 5, 2, 4, 1, 5, 2, 4, 6, 5]
        self.right =[5, 1, 3, 4, 5, 1, 3, 4, 5, 1, 3, 4, 5, 1, 3, 4, 5, 1, 0, 6, 4]
        self.real = [self.left, self.center, self.right]
        self.real_pos = [0, 0, 0]# リール上の現在の中心位置 [left, center, right]
        self.real_run = [0, 0, 0]# リールが動いているか     [left, center, right]
        
        # ↓役とその点数↓
        self.roles = {(0, 0, 0):"REG", (0, 0, 6):"REG", (0, 6, 0):"REG", (6, 0, 0):"REG", (1, 1, 1):"bell", (3, 3, 3):"clown", (4, 4, 4):"mascot", (5, 5, 5):"replay", (6, 6, 6):"BIG"}
        self.scores = {"REG":2, "BIG":3, "bell":1, "clown":1, "mascot":1, "cherry":1, "hazure":0}
        self.score = 0
        self.highest = self.score
    
    def reset(self, game_count = 5):
        self.game_count = game_count
        self.score = 0
        print("reset")
    
    def start(self):
        if self.game_count > 0:
            self.real_run = [1, 1, 1]
            self.state = "Run"
            print("start")
        else:
            print("ゲームの残り回数が0です")

    def rotate(self):
        for i in range(3):
            if self.real_run[i] == 1:
                self.real_pos[i] = (self.real_pos[i]+1)%self.tile_num

    def stop(self, real):
        if self.real_run[real] == 1:
            self.real_run[real] = 0
            if self.real_run == [0, 0, 0]:
                self.finish()
        
    def finish(self):
        result = self.check_role()
        if result == "replay":
            self.start()# リプレイのみ別処理
        else:
            self.cashback(result)
            self.game_count -= 1
        if self.score > self.highest:
            self.highest = self.score
        self.state = "Wait"
        
    def check_role(self):
        result = np.array([[self.real[i][(self.real_pos[i]+j)%self.tile_num] for i in range(3)] for j in [-1, 0, 1]])
        rup = [result[0, 0], result[1, 1], result[2, 2]]
        rdwn = [result[2, 0], result[1, 1], result[0, 2]]
        lines = np.concatenate([result, [rup], [rdwn]])# up, mid, btm, rup, rdwn
        #print(named:= [[self.image_name[num] for num in row] for row in result_])
        for line in lines:
            for roll in list(self.roles.keys()):
                if np.all(line == roll):
                    return self.roles[roll]
            if line[0] == 2 and line[1] == 2:
                return "cherry"# cherryのみ2個でそろう(同時に二つそろう場合は他が優先される)
        return "hazure"

    def cashback(self, role):
        self.score += self.scores[role]
        print(f"{self.scores[role]}ポイント獲得！")
    
    def draw(self, screen):        
        screen.blit(self.images[self.left[(self.real_pos[0]+1)%self.tile_num]], (0, 20))
        screen.blit(self.images[self.left[self.real_pos[0]]], (0, 170))
        screen.blit(self.images[self.left[self.real_pos[0]-1]], (0, 320))
        
        screen.blit(self.images[self.center[(self.real_pos[1]+1)%self.tile_num]], (310, 20))
        screen.blit(self.images[self.center[self.real_pos[1]]], (310, 170))
        screen.blit(self.images[self.center[self.real_pos[1]-1]], (310, 320))
        
        screen.blit(self.images[self.right[(self.real_pos[2]+1)%self.tile_num]], (620, 20))
        screen.blit(self.images[self.right[self.real_pos[2]]], (620, 170))
        screen.blit(self.images[self.right[self.real_pos[2]-1]], (620, 320))
        
    def draw_7seg(self, screen, right, top, val):
        for i, num in enumerate(list(str(val))[::-1]):
            screen.blit(self.image_num[int(num)], (-(i+1)*self.seg_size[0]+right, top))    

def main():
    ### シリアル通信 ###
    if Arduino:
        ser = serial.Serial()
        ser.port = "COM4"# ArduinoIDEから要確認
        ser.baudrate = 9600# Arduino側と合わせる
        ser.timeout = 0
        ser.open()
        ser.readline()# ArduinoIDEでシリアルモニターを開いているとエラーを吐く
    ### pygame ###
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    fps = 120# 上限fps
    tick = 0
    tickrate = 13
    difficulty = 2
    slot = MySlot()
    while True:
        ### 描画処理 ###
        screen.fill((0, 0, 0))
        slot.draw(screen)
        slot.draw_7seg(screen, WIDTH, 490, slot.game_count)
        slot.draw_7seg(screen, WIDTH/2, 490, slot.score)
        
        ### ゲーム処理 ###
        if tick == tickrate:
            tick = 0
            if slot.state == "Wait":
                continue
            elif slot.state == "Run":
                slot.rotate()
        
        ### ボタン処理(Arduino) ###
        if Arduino:
            button = ser.readline()
            #print(button)
            if button == b"left\r\n":
                slot.stop(Left)
            if button == b"center\r\n":
                slot.stop(Left)
            if button == b"right\r\n":
                slot.stop(Left)
            if button == b"start\r\n" and slot.state == "Wait":
                slot.start(Left)                
        
        for event in pygame.event.get():
            ### ボタン処理 ###
            if event.type == KEYDOWN:
                if slot.state == "Wait":
                    if event.key == K_RETURN:
                        slot.reset()
                    if event.key == K_SPACE:
                        slot.start()
                elif slot.state == "Run":
                    if event.key == K_a:
                        slot.stop(Left)
                    if event.key == K_s:
                        slot.stop(Center)
                    if event.key == K_d:
                        slot.stop(Right)
                if event.key == K_3:
                    tickrate = 10
                    difficulty = 3
                    print(f"難易度:{difficulty}")
                if event.key == K_2:
                    tickrate = 13
                    difficulty = 3
                    print(f"難易度:{difficulty}")
                if event.key == K_1:
                    tickrate = 16
                    difficulty = 3
                    print(f"難易度:{difficulty}")
                '''テストプレイ用の細かいスピード調節
                if event.key == K_UP:
                    tickrate -= 1
                    print(tickrate)
                if event.key == K_DOWN:
                    tickrate += 1
                    print(tickrate)
                #'''
                    
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        tick += 1
        clock.tick(fps)
        pygame.display.update()

if __name__ == "__main__":
    main()