#include <ax12.h>

const int LEFT = 3;
const int RIGHT = 2;
const int HIPS = 5;

const int SPEED = 5;

const int LR_STEP = 60;
const int INIT_POS = 512;
const int HIPS_STEP = 200;

void setup(){
  SetPosition(HIPS, INIT_POS);
  SetPosition(LEFT, INIT_POS);
  SetPosition(RIGHT, INIT_POS);
  delay(1000);
}

void loop(){
  goTo(1, INIT_POS + LR_STEP, INIT_POS + LR_STEP);
  delay(1000);
  goTo(0, INIT_POS - LR_STEP, INIT_POS - LR_STEP);
  delay(1000);
}

void goTo(boolean leftUp, int finalLeft, int finalRight){
  int initLeft = GetPosition(LEFT);
  int initRight = GetPosition(RIGHT);
  int maxChange;
  
  if(leftUp)
    SetPosition(HIPS, INIT_POS - HIPS_STEP);
  else
    SetPosition(HIPS, INIT_POS + HIPS_STEP);
  
  if (abs(finalRight - initRight) > abs(finalLeft - initRight))
    maxChange = finalRight - initRight;
  else
    maxChange = initLeft - finalLeft;
  
  for(int i = 0; i < abs(maxChange); i+=SPEED){
    if(finalRight > initRight){
      if(GetPosition(RIGHT) < finalRight)
        SetPosition(RIGHT, GetPosition(RIGHT)+SPEED);
    }else{
      if(GetPosition(RIGHT) > finalRight)
        SetPosition(RIGHT, GetPosition(RIGHT)-SPEED);
    }
    
    if(finalLeft > initLeft){
      if(GetPosition(LEFT) < finalLeft)
        SetPosition(LEFT, GetPosition(LEFT)+SPEED);
    }else{
      if(GetPosition(LEFT) > finalLeft)
        SetPosition(LEFT, GetPosition(LEFT)-SPEED);
    }
  }
}
