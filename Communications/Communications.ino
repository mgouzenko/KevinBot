#include <ax12.h>
#include <BioloidController.h>

const int IN_PACKET_SIZE = 7;
const int CHECK_MOD = 240;
const int PACKET_START = 255;

const int CENTER = 512;
const int SPEED = 5;
const int HIPS_STEP = 200;

const int LEFT_SERV = 2;
const int RIGHT_SERV = 1;
const int HIPS_SERV = 3;

int left_goto;
int left_cur;
int right_goto;
int right_cur;
int hips_goto;
int hips_cur;
int smooth_walk;
int enabled;
int checked=0;
int test;

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
  if (enabled){
    SetPosition(HIPS_SERV, hips_goto);
    hips_cur = hips_goto;
    
    if(smooth_walk){
      //speed may be too fast. If so, make movement occur every nth cycle
      int dir;
      if (left_goto == left_cur) dir = 0;
      else if(left_goto > left_cur) dir = 1;
      else dir = -1;
      SetPosition(LEFT_SERV, left_cur + dir*SPEED);
      left_cur = left_cur + dir*SPEED;
      
      if (right_goto == right_cur) dir = 0;
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
  }
  comm_read();
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
  check_sum += (hips_cur)/4;
  check_sum += (int)('t');
  check_sum += (int)('b');
  check_sum += bits;
  check_sum = check_sum % CHECK_MOD;
  
  Serial.write(char(PACKET_START));
  Serial.write(char((left_cur)/4));
  Serial.write(char((right_cur)/4));
  Serial.write(char((hips_cur)/4)); //random filler (turret)
  Serial.write('t'); //random filler (turret)
  Serial.write('b'); //random filler (battery)
  Serial.write(char(bits));
  Serial.write(char(check_sum));
}

void comm_read(){
  int bits;
  if(Serial.available() >= IN_PACKET_SIZE  &&  Serial.read() == PACKET_START){
    byte v1=Serial.read();
    byte v2=Serial.read();
    byte v3=Serial.read();
    byte v4=Serial.read();
    byte v5=Serial.read();
    byte cs=Serial.read();
    int sum=int(v1);
    sum+=int(v2);
    sum+=int(v3);
    sum+=int(v4);
    sum+=int(v5);

    while (sum>=240)
      sum-=240;
      
    if(sum == cs){
      left_goto = 4*(int)(v1);
      right_goto = 4*(int)(v2);
      //turret variable 1 v3
      //turret_variable 2 v4
      bits = v5;
      
      bits /= 2; //filler
      bits /= 2; //filler
      bits /= 2; //laser toggle
      //enabled = bits%2;
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
      comm_write();
    }
  }
}
