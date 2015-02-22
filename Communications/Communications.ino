#include <ax12.h>
#include <BioloidController.h>

const int IN_PACKET_SIZE = 7;
const int CHECK_MOD = 240;
const int PACKET_START = 255;

const int CENTER = 512;
const int SPEED = 5;
const int HIPS_STEP = 200;

const int LEFT_SERV = 3;
const int RIGHT_SERV = 2;
const int HIPS_SERV = 5;

int left_goto;
int left_cur;
int right_goto;
int right_cur;
int hips_goto;
int hips_cur;
int smooth_walk;
int enabled;

void setup(){
  Serial.begin(38400);
  SetPosition(HIPS_SERV, CENTER);
  SetPosition(LEFT_SERV, CENTER);
  SetPosition(RIGHT_SERV, CENTER);
  left_cur = right_cur = hips_cur = CENTER;
  left_goto = right_goto = hips_goto = CENTER;
  smooth_walk = 0;
  enabled = 1;
  delay(1000);
}

void loop(){
  while(true){ // I apologize for the messy indenting
    comm_read();
    if(!enabled){
      comm_write();
      continue;
    }
    
    SetPosition(HIPS_SERV, hips_goto);
    hips_cur = hips_goto;
    
    if(smooth_walk){
      //speed may be too fast. If so, make movement occur every nth cycle
      int dir;
      if (left_goto == left_cur) dir = 0
      else if(left_goto > left_cur) dir = 1;
      else dir = -1;
      SetPosition(LEFT_SERV, left_cur + dir*SPEED);
      left_cur = left_cur + dir*SPEED;
      
      if (right_goto == right_cur) dir = 0
      else if(right_goto > right_cur) dir = 1;
      else dir = -1;
      SetPosition(RIGHT_SERV, right_cur + dir*SPEED);
      right_cur = right_cur + dir*SPEED;
    }else{//JERKY WALKING, BOY
      SetPosition(RIGHT_SERV, right_goto);
      right_cur = right_goto;
      
      SetPosition(LEFT_SERV, left_goto);
      left_cur = left_goto;
    }
    
    comm_write();
    
  }  
}

void comm_write(){
  unsigned int check_sum = 0;
  int bits = 0;
  
  int hip_bit_dec = 0;
  if(hips_cur == CENTER + HIPS_STEP)
    hip_bit_dec = 1;
  else if(hips_cur == CENTER - HIPS_STEP)
    hip_bit_dec = 2;
  bits += hip_bit_dec * 2^6;
  
  check_sum += (left_cur)/4;
  check_sum += (right_cur)/4;
  check_sum += (int)('t');
  check_sum += (int)('t');
  check_sum += (int)('b');
  check_sum += bits;
  check_sum = check_sum % CHECK_MOD;
  
  Serial.write((char)PACKET_START);
  Serial.write((char)((left_cur)/4));
  Serial.write((char)((right_cur)/4));
  Serial.write('t'); //random filler (turret)
  Serial.write('t'); //random filler (turret)
  Serial.write('b'); //random filler (battery)
  Serial.write((char)bits);
  Serial.write((char)check_sum);
  
  

}

void comm_read(){
  int bits;
  if(Serial.available() >= IN_PACKET_SIZE  &&  Serial.read() == PACKET_START){
    
    byte in[IN_PACKET_SIZE-2];
    for(int i=0; i < IN_PACKET_SIZE-2; ++i){
      in[i] = Serial.read();
    }
    
    int check_sum = (int)(Serial.read());
    unsigned int sum = 0;
    for(int i = 0; i < IN_PACKET_SIZE-2; ++i){
      sum += (int)(in[i]);
    }
    
    if(sum == check_sum){
      left_goto = 4*(int)(in[0]);
      right_goto = 4*(int)(in[1]);
      //turret variable 1 in[2]
      //turret_variable 2 in[3]
      bits = in[3];
      
      bits /= 2; //filler
      bits /= 2; //filler
      bits /= 2; //laser toggle
      enabled = bits%2;
      bits /= 2;
      int temp = bits%4;
      bits /= 4;
      smooth_walk = bits%2;
      bits /= 2;
      bits /= 2; //fire!
      
      if(temp == 1) //this SHOULD be right leg up
        hips_goto = CENTER + HIPS_STEP;
      else if(temp == 2) //this SHOULD be left leg up
        hips_goto = CENTER - HIPS_STEP;
      else
        hips_goto = CENTER;
    }
  }
}
