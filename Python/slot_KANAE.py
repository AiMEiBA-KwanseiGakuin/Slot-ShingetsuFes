# made by 金栄智治
import numpy as np
import pygame,sys
from pygame.locals import *
import serial


WIDTH,HEIGHT=920,490+200
Left,Center,Right=0,1,2
Opening,Running,Finished=0,1,2

class Slot(pygame.sprite.Sprite):
    rad=np.random.default_rng()
    def __init__(self):
        super().__init__()
        self.num=21         #リールのタイル数
        self.height=150     #タイルの縦横幅
        self.width=300
        '''
        # ↓役とその確率↓ set_flagで使用予定
        self.roles=["BIG","REG","bell","juggler","mascat","replay","cerry","HAZURE"]
        self.roles_={"BIG":[6,6,6],"bell":[1,1,1],"juggler":[3,3,3],"mascat":[4,4,4],"replay":[5,5,5],"cerry":[2,2]}
        p_list=1/np.array([273.07,439.84,1092,1092.27,6.024,7.298,35.62])#+はずれ
        self.p_table=np.concatenate([p_list,[1-np.sum(p_list)]])
        '''
        # ↓画像読み込み↓    0      1      2       3          4       5        6
        self.image_name=["bar","bell","cerry","juggler","mascat","replay","seven"]
        self.images=[pygame.image.load(name+".jpeg").convert_alpha() for name in self.image_name]
        self.images=[pygame.transform.scale(image,(self.width,self.height)) for image in self.images]
        self.image_num=[pygame.image.load(str(num)+".jpg").convert_alpha() for num in range(10)]#7セグ用
        self.image_num=[pygame.transform.scale(image,(135,200)) for image in self.image_num]#7セグ用
        
        # ↓image_nameと対応する画像の順番↓
        self.left=  [4,5,4,0,2,4,5,4,3,6,4,5,4,2,0,4,5,4,5,6,1]
        self.center=[3,2,4,0,5,2,4,1,5,2,4,0,5,2,4,1,5,2,4,6,5]
        self.right= [5,1,3,4,5,1,3,4,5,1,3,4,5,1,3,4,5,1,0,6,4]
        self.real=[self.left,self.center,self.right]
        self.real_pos=[0,0,0]# リール上の現在の位置(中心) [left,center,right]
        self.real_run=[0,0,0]# リールが動いているか
        #self.stopping=["","",""]
        # ↓もろもろの状態変数など↓
        self.canstart=False  #開始条件
        self.state=Opening
        #self.flag=None      # 事前抽選するフラグ用(set_flagで使用予定)
        #self.bonus=False    # ボーナス状態(未実装)
        self.count=0         # 投入金額や払い出し金額のカウント用?(未使用?)
        self.g_count=5

    def start(self):# ゲーム開始時に呼び出し
        if self.canstart and self.g_count>0:
            self.real_run=[1,1,1]
            #self.set_flag()
            self.state=Running
    '''
    def set_flag(self):# フラグ抽選(未使用,slidestopと合わせて運用予定)
        if self.bonus==False:
            self.flag=self.rad.choice(self.roles,p=self.p_table)
        else:
            self.flag="BIG"
        #print(self.flag)
    '''
    def finish(self):# ゲーム終了
        self.canstart=False
        #self.flag=None
        self.state=Opening
        self.g_count-=1
    
    def draw(self,screen):# 画像描画
        screen.blit(self.images[self.left[(self.real_pos[0]+1)%self.num]],(0,20))
        screen.blit(self.images[self.left[self.real_pos[0]]],(0,170))
        screen.blit(self.images[self.left[self.real_pos[0]-1]],(0,320))
        
        screen.blit(self.images[self.center[(self.real_pos[1]+1)%self.num]],(310,20))
        screen.blit(self.images[self.center[self.real_pos[1]]],(310,170))
        screen.blit(self.images[self.center[self.real_pos[1]-1]],(310,320))
        
        screen.blit(self.images[self.right[(self.real_pos[2]+1)%self.num]],(620,20))
        screen.blit(self.images[self.right[self.real_pos[2]]],(620,170))
        screen.blit(self.images[self.right[self.real_pos[2]-1]],(620,320))
        
    def draw_7seg(self,screen,left,top,val:"int"):
        for i,num in enumerate(list(str(val))):
            screen.blit(self.image_num[int(num)],(left+(i*140),top))
    
    def rotete(self):# リール回転
        for i in range(3):
            if self.real_run[i]==1:
                self.real_pos[i]=(self.real_pos[i]+1)%self.num

    def stop(self,real):# リール停止(全てのリールが止まったら終了処理に移行)
        if self.real_run[real]==1:
            self.real_run[real]=0
            if self.real_run==[0,0,0]:
                self.state=Finished
    '''
    def slidestop(self,real):# フラグに合わせる停止処理(未実装)
        
    '''
    def choose_role(self):# 全リール停止後(slidestop内でも使うかも?)の役判定
        result=np.array([
        [self.left[self.real_pos[0]-1%self.num], self.center[self.real_pos[1]-1%self.num], self.right[self.real_pos[2]-1%self.num]],
        [self.left[self.real_pos[0]], self.center[self.real_pos[1]], self.right[self.real_pos[2]]],
        [self.left[(self.real_pos[0]+1)%self.num], self.center[(self.real_pos[1]+1)%self.num], self.right[(self.real_pos[2]+1)%self.num]]])
        # ↓可読性0バージョン↓
        result_=np.array([[self.real[i][(self.real_pos[i]+j)%self.num] for i in range(3)] for j in [-1,0,1]])
 
        rup=[result[0,0],result[1,1],result[2,2]]
        rdwn=[result[2,0],result[1,1],result[0,2]]
        lines=np.concatenate([result,[rup],[rdwn]])# up,mid,btm,rup,rdwn
        #print(named:=[[self.image_name[num] for num in row] for row in result_])
        for line in lines:
            if np.all(line==[1,1,1]):    #bell
                print("bell!")
                self.cashback(15)
            if line[0]==2 and line[1]==2:#cherry
                print("cherry!")
                self.cashback(2)
            if np.all(line==[3,3,3]):    #juggler
                print("juggler!")
                self.cashback(10)
                print("juggler!")
            if np.all(line==[4,4,4]):    #mascot
                print("mascot!")
                self.cashback(7)
            if np.all(line==[5,5,5]):    #replay
                print("replay!")
                self.cashback(0)
                self.start()
            if np.all(line==[6,6,6]):    #BIG
                print("BIG!")
                self.cashback(250,1)
            if np.all(line==[0,0,0]) or np.all(line==[6,0,6]) or np.all(line==[6,6,0]) or np.all(line==[0,6,6]):#REG
                print("REG!")
                self.cashback(50)

    def cashback(self,val,seven=0):# 払い戻し
        #self.d_count=val#7セグ表示用のやつ 描画時にd_count=0になるまで1フレームづつcount+=1する予定
        self.count+=1#val
        if seven:self.count+=1
        print(f"${val} cashbacked!!")
    
def main():
    # ↓シリアル通信↓
    ser = serial.Serial()
    ser.port="COM5"     #デバイスマネージャでArduinoのポート確認
    ser.baudrate=9600  #Arduinoと合わせる
    ser.open()
    ser.readline()
    # ↓pygame初期化など↓
    pygame.init()
    screen=pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("ジャグラー")
    clock=pygame.time.Clock()
    speed=60
    ### リール回転速度
    myslot=Slot()
    
    while True:
        ## 描画処理 ##
        screen.fill((0,0,0))
        myslot.draw(screen)
        myslot.draw_7seg(screen,780,490,myslot.g_count)
        myslot.draw_7seg(screen,200,490,myslot.count)
        
        ## ゲーム処理 ##
        if myslot.state==Opening:#   待機状態
            myslot.start()
        
        elif myslot.state==Running:#  リール回転中
            myslot.rotete()
        
        elif myslot.state==Finished:# 全リール停止時
            myslot.choose_role()
            myslot.finish()
            
        button=ser.readline()
        if button==b'left\r\n':
            myslot.stop(Left)
        elif button==b'center\r\n':
            myslot.stop(Center)
        elif button==b'right\r\n':
            myslot.stop(Right)
        elif button==b'start\r\n' and myslot.state==Opening:
            myslot.canstart=True
 
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type==KEYDOWN:
                if myslot.state==Opening and event.key==K_RETURN:
                    #myslot.canstart=True
                    myslot.g_count=5
                    myslot.count=0

                if myslot.state==Running:
                    if event.key==K_a:
                        myslot.stop(Left)
                        #myslot.slidestop("left")
                    if event.key==K_s:
                        myslot.stop(Center)
                        #myslot.slidestop("center")
                    if event.key==K_d:
                        myslot.stop(Right)
                        #myslot.slidestop("right")
                    
        clock.tick(speed)
        pygame.display.update()

if __name__=="__main__":
    main()