/***************************
 * AXSimpleTest
 * This sketch sends positional commands to the AX servo 
 * attached to it - the servo must set to ID # 1
 * The sketch will send a value, i, to the servo.
 * 'For' loops are used to increment and decrement the value of 'i'
 ***************************/

//import ax12 library to send DYNAMIXEL commands
#include <ax12.h>


//serial numbers
const int LEFT = 3;
const int RIGHT = 2;
const int HIPS = 5;

const int LR_STEP = 60;
const int INIT_POS = 512;
const int HIPS_STEP = 200;

void setup(){
    SetPosition(LEFT, INIT_POS);
    SetPosition(RIGHT, INIT_POS);
    SetPosition(HIPS, INIT_POS);
    delay(2000);
}

void loop(){
    SetPosition(HIPS, INIT_POS + HIPS_STEP);
    delay(500);
    SetPosition(LEFT, INIT_POS + LR_STEP);
    SetPosition(RIGHT, INIT_POS + LR_STEP);
        
    delay(1000);

    SetPosition(HIPS, INIT_POS - HIPS_STEP);
    delay(500);
    SetPosition(LEFT, INIT_POS - LR_STEP);
    SetPosition(RIGHT, INIT_POS - LR_STEP);
    
    delay(1000);
}
