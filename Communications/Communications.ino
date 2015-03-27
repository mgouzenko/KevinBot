#include <ax12.h>
#include <BioloidController.h>

const int IN_PACKET_SIZE = 7;
const int CHECK_MOD = 240;
const int PACKET_START = 255;

const int CENTER = 512;
const int SPEED = 5;
const float STRIDE = .4;
const int HIPS_STEP = 300;

const int PLIMIT = 300;
const int TLIMITUP = 600;
const int TLIMITDOWN = 480;
const int TCENTER = 512;
const float ROTATION = .01;

const int LEFT_SERV = 3;
const int RIGHT_SERV = 1;
const int HIPS_SERV = 2;
const int PAN_SERV = 4;
const int TILT_SERV = 5;

const int GUN_PIN = 7;

int x;
int y;
int p;
int t;
int hipSwitch;
int left_goto;
int left_cur;
int right_goto;
int right_cur;
int hips_goto;
int hips_cur;
int pan_cur;
int tilt_cur;
int fire = 0;
int smooth_walk;
int enabled;
int test=0;

void setup(){
  Serial.begin(38400);
  pinMode(GUN_PIN,OUTPUT);
  digitalWrite(GUN_PIN,LOW);
  
  SetPosition(HIPS_SERV, CENTER);
  SetPosition(LEFT_SERV, CENTER);
  SetPosition(RIGHT_SERV, CENTER);
  left_cur = right_cur = hips_cur = pan_cur = CENTER;
  left_goto = right_goto = hips_goto = CENTER;
  tilt_cur = TCENTER;
  smooth_walk = 0;
  enabled = 1;
  delay(1000);
}

void loop(){
  if (enabled){
    if(hipSwitch == 1){ //this SHOULD be right leg up
      hips_goto = CENTER - HIPS_STEP;
      left_goto = CENTER - y;
      right_goto = CENTER - x - y;
    }else if(hipSwitch == 2){ //this SHOULD be left leg up
      hips_goto = CENTER + HIPS_STEP;
      left_goto = CENTER -x + y;
      right_goto = CENTER + y;
    }else{
      hips_goto = CENTER;
    }
    SetPosition(HIPS_SERV, hips_goto);
    hips_cur = hips_goto;
    delay(1);
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
      delay(1);
      
      SetPosition(LEFT_SERV, left_goto);
      left_cur = left_goto;
      delay(1);
    }
    tilt_cur+=t;
    pan_cur-=p;
    if (tilt_cur>TLIMITUP)
      tilt_cur=TLIMITUP;
    if (tilt_cur<TLIMITDOWN)
      tilt_cur=TLIMITDOWN;
    if (pan_cur>CENTER+PLIMIT)
      pan_cur=CENTER+PLIMIT;
    if (pan_cur<CENTER-PLIMIT)
      pan_cur=CENTER-PLIMIT;
    SetPosition(TILT_SERV, tilt_cur);
    delay(1);
    SetPosition(PAN_SERV, pan_cur);
    delay(1);
    digitalWrite(GUN_PIN,fire);
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
  check_sum += test;
  check_sum += (int)('t');
  check_sum += (int)('b');
  check_sum += bits;
  check_sum = check_sum % CHECK_MOD;
  
  Serial.write(char(PACKET_START));
  Serial.write(char((left_cur)/4));
  Serial.write(char((right_cur)/4));
  Serial.write(char(test)); //random filler (turret)
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
      y = int(STRIDE*float((int)(v1)-128));
      x = int(STRIDE*float((int)(v2)-128));
      t = int(ROTATION*float((int)(v3)-128));
      p = int(ROTATION*float((int)(v4)-128));
      bits = v5;
      test = bits;
      bits /= 2; //filler
      bits /= 2; //filler
      bits /= 2; //laser toggle
      //enabled = bits%2;
      bits /= 2;
      hipSwitch = bits%4;
      bits /= 4;
      smooth_walk = bits%2;
      bits /= 2;
      fire = bits%2;
      test = fire;
      bits /= 2; //fire!
      
      comm_write();
    }
  }
}
