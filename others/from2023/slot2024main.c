#include <stdio.h>
#include <assert.h>
#include "slot2024.h"
//設定ごとの確率設定{big,reg,チェリー,リプレイ,ブドウ}
int flug_l[2][5] = { {1,1,7,34,40},{2,2,9,34,42} };b=


int main(void){
    int b_flug;  //ボーナス状態の保存
    int stop[3]; //停止位置の保存
    int medal;
    int

    int rand = getrand();
    printf("%d\n",rand);
    int lot = 0;
    int flug = flugcheck(rand, flug_l,lot);
    printf("%d",flug);
    int c
    for (int i=0;i<2;i++){
        while (/*ardinoでボタンが押された判定の信号をもらった時*/ ){
        c = 0; 
        }
        stop[i] /*=押されたボタンの位置*/ ;
        reel(stop[i],c);
    }
    medal += add_medal(flug);

    


}