#include <ax12.h>
#include <BioloidController.h>

const int LEFT = 3;
const int RIGHT = 2;
const int HIPS = 5;

const int SPEED = 5;

const int LR_STEP = 60;
const int INIT_POS = 512;
const int HIPS_STEP = 200;

char x = 128;
char y = 128;
char h = 0;

void setup(){
  Serial.begin(38400);
  SetPosition(HIPS, INIT_POS);
  SetPosition(LEFT, INIT_POS);
  SetPosition(RIGHT, INIT_POS);
  delay(1000);
}

void loop(){
  comm();
  if (h)
    goTo(h, INIT_POS + x - 128, INIT_POS + y - 128);
  else
    goTo(h, INIT_POS + y - 128, INIT_POS + x - 128);
  delay(50);
}

void comm(){
  if (Serial.available()>=5 && Serial.read()==255){
    char v1=Serial.read();
    char v2=Serial.read();
    char v3=Serial.read();
    char sum=v1+v2+v3;
    if (sum==Serial.read()){
      x=v1;
      y=v2;
      h=v3;
    }
  }
  Serial.write(255);
  Serial.write(x);
  Serial.write(y);
  Serial.write(h);
  Serial.write(x+y+h);
  delay(20);
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
