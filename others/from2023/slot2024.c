#include <stdio.h>
#include <assert.h>
#include <stdlib.h>
#include <time.h>
#include "slot2024.h"


int getrand(void){
    srand((unsigned int)time(NULL));
    return rand()%256 + 1;
}

int flugcheck(int x,int y[][5],int z){
    int i,j;
    for(i=0;i<4;i++){
        x - y[z][i];//減算式
        if (x<=0){
            return i;
        }
    }
    return 6;//はずれ対応
}

void reel(int[],int){//リール制御用
    return 0;
}

int add_medal( int flug){
    
}