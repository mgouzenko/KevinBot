#include <ax12.h>
#include <BioloidController.h>


/***************************
 * AXSimpleTest
 * This sketch sends positional commands to the AX servo 
 * attached to it - the servo must set to ID # 1
 * The sketch will send a value, i, to the servo.
 * 'For' loops are used to increment and decrement the value of 'i'
 ***************************/

//import ax12 library to send DYNAMIXEL commands
#include <ax12.h>
#include <BioloidController.h>


//serial numbers
const int LEFT = 3;
const int RIGHT = 2;
const int HIPS = 5;

const int LR_STEP = 60;
const int INIT_POS = 512;
const int HIPS_STEP = 200;

#ifndef DROID_POSES
#define DROID_POSES

#include <avr/pgmspace.h>

PROGMEM prog_uint16_t testPos1[] = {4, 512, 512, 512, 300};
PROGMEM prog_uint16_t testPos2[] = {4, 700, 700, 700, 800};
PROGMEM prog_uint16_t testPos3[] = {4, 300, 300, 300, 250};
PROGMEM prog_uint16_t testPos4[] = {4, 800, 800, 800, 850};

PROGMEM transition_t forward[] = {{testPos1,2000}, {testPos2,2000}, {testPos3,2000}, {testPos4,2000}};

#endif

#include <ax12.h>
#include <BioloidController.h>
//#include "poses.h"  // pose file generated from PyPose

BioloidController bioloid = BioloidController(1000000);

#define frames 6
int idx = 0;



void setup(){    
    delay(100);                    // recommended pause
//  bioloid.loadPose(testPos1);   // load the pose from FLASH, into the nextPose buffer
    bioloid.readPose();            // read in current servo positions to the curPose buffer
    bioloid.interpolateSetup(500); // setup for interpolation from current->next over 1/2 a second
    while(bioloid.interpolating > 0){  // do this while we have not reached our new pose
        bioloid.readPose();
        bioloid.interpolateStep();     // move servos, if necessary. 
        delay(3);
    }
    bioloid.playSeq(forward);
}

void loop(){
  bioloid.play();
  bioloid.play();
  bioloid.play();
}

