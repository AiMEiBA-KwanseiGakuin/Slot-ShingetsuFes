### インポート
import sys
import pygame
from pygame.locals import *

############################
### 詳細設定
############################
SURFACE = Rect(0,0,600,300)    # 画面サイズ(X軸,Y軸,横,縦)
W_TIME  = 20                  # 待ち時間
pt_width = 200
pt_height = 100 

############################
### スプライトクラス継承 
############################
class MySprite(pygame.sprite.Sprite):

    ############################
    ### 初期化メソッド(ファイル名,横の長さ,縦の長さ)
    ############################
    def __init__(self, name,x,y, x_size, y_size,):
        pygame.sprite.Sprite.__init__(self)

        ### 透過変換でファイル読み込み
        self.image = pygame.image.load(name).convert_alpha()

        ### 画像サイズ変更
        self.image = pygame.transform.scale(self.image, (x_size,y_size))

        ### 画像サイズ取得
        self.width  = self.image.get_width()
        self.height = self.image.get_height()
        ### 四角形オブジェクト生成
        self.rect = Rect(x, y, self.width, self.height)

    ############################
    ### クリック確認
    ############################
    def check(self, pos):
        return self.rect.collidepoint(pos)

    ############################
    ### オブジェクト描画
    ############################
    def draw(self, surface):
        surface.blit(self.image, self.rect)


###########################
###回転処理####
###########################
pt_list=["bar.jpeg","bell.jpeg","cerry.jpeg","juggler.jpeg","mascat.jpeg","replay.jpeg","seven.jpeg"]   ###画像のリスト
pt_list2=["bar.jpeg","bell.jpeg","cerry.jpeg","cerry.jpeg","juggler.jpeg","mascat.jpeg","replay.jpeg","seven.jpeg"]
pt_list3=["bar.jpeg","bell.jpeg","cerry.jpeg","juggler.jpeg","mascat.jpeg","replay.jpeg","seven.jpeg"]
i=0
j=0
k=0

def Loop1(flag):
    global i
    pt1_1 = MySprite(pt_list[i%len(pt_list)],0,0, pt_width, pt_height)
    pt1_2 = MySprite(pt_list[(i+1)%len(pt_list)],0,pt_height, pt_width, pt_height)
    pt1_3 = MySprite(pt_list[(i+2)%len(pt_list)],0,2*pt_height, pt_width, pt_height)
    pt1_1.draw(surface)
    pt1_2.draw(surface)
    pt1_3.draw(surface)

def Loop2(flag):
    global j
    pt2_1 = MySprite(pt_list2[j%len(pt_list2)],pt_width,0, pt_width, pt_height)
    pt2_2 = MySprite(pt_list2[(j+1)%len(pt_list2)],pt_width,pt_height, pt_width, pt_height)
    pt2_3 = MySprite(pt_list2[(j+2)%len(pt_list2)],pt_width,2*pt_height, pt_width, pt_height)
    pt2_1.draw(surface)
    pt2_2.draw(surface)
    pt2_3.draw(surface)

def Loop3(flag):
    global k
    pt3_1 = MySprite(pt_list3[k%len(pt_list3)],2*pt_width,0, pt_width, pt_height)
    pt3_2 = MySprite(pt_list3[(k+1)%len(pt_list3)],2*pt_width,pt_height, pt_width, pt_height)
    pt3_3 = MySprite(pt_list3[(k+2)%len(pt_list3)],2*pt_width,2*pt_height, pt_width, pt_height)
    pt3_1.draw(surface)
    pt3_2.draw(surface)
    pt3_3.draw(surface)

############################
### メイン関数 
############################
def main():

    ### 変数初期化
    global i 
    global j
    global k
    flag1 = False
    flag2 = False
    flag3 = False

    ### 画面初期化
    pygame.init()
    global surface
    surface = pygame.display.set_mode(SURFACE.size)

    ### 無限ループ
    while True:

        ### 背景色設定
        surface.fill((0,0,0))

        ### 回転
        Loop1(flag1)
        Loop2(flag2)
        Loop3(flag3)

        if not flag1:
            i += 1
        if not flag2:
            j += 1
        if not flag3:
            k += 1

        ### 画面更新
        pygame.display.update()

        ### ウエイト
        pygame.time.wait(W_TIME)

        ### イベント処理
        for event in pygame.event.get():

            ### マウスボタンイベント
            if event.type == MOUSEBUTTONDOWN:
                flag1 = True
            if event.type == KEYDOWN:
                if event.key == K_a:
                    flag1 = True
                if event.key == K_s:
                    flag2 = True
                if event.key == K_d:
                    flag3 = True

            ### 終了処理
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

############################
### メイン関数呼び出し
############################
if __name__ == "__main__":
    main()
