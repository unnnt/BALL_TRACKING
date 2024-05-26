// Motor depan          BAWAH KE ATAS
#define EN1 4          //KANAN-D
#define IN1 64
#define IN2 36
#define IN3 12
#define IN4 2
#define EN2 9          //KIRI-D

// Motor belakang       LUAR KE DALAM
#define EN3 3          //KANAN-B
#define IN5 11
#define IN6 6
#define IN7 8
#define IN8 10
#define EN4 7          //KIRI-B


int maju[]        = {1 , 0 , 1 , 0 , 1 , 0 , 1 , 0};
int curve_kanan[] = {1 , 0 , 1 , 0 , 1 , 0 , 1 , 0};
int curve_kiri[]  = {1 , 0 , 1 , 0 , 1 , 0 , 1 , 0};
int kanan[]       = {0 , 1 , 1 , 0 , 1 , 0 , 0 , 1};
int kiri[]        = {1 , 0 , 0 , 1 , 0 , 1 , 1 , 0};
int mundur[]      = {0 , 1 , 0 , 1 , 0 , 1 , 0 , 1};
int rot_kiri[]    = {1 , 0 , 0 , 1 , 1 , 0 , 0 , 1};
int rot_kanan[]   = {0 , 1 , 1 , 0 , 0 , 1 , 1 , 0};
int stopp[]       = {0 , 0 , 0 , 0 , 0 , 0 , 0 , 0};


int pinMotor(int index) {
  switch (index) {
    case 0:
      return IN1;
    case 1:
      return IN2;
    case 2:
      return IN3;
    case 3:
      return IN4;
    case 4:
      return IN5;
    case 5:
      return IN6;
    case 6:
      return IN7;
    case 7:
      return IN8;
    default:
      return -1;
  }
}

void setup_pinmotor() {
  pinMode(EN1, OUTPUT); pinMode(IN1, OUTPUT);  pinMode(IN2, OUTPUT); pinMode(IN3, OUTPUT);  pinMode(IN4, OUTPUT); pinMode(EN2, OUTPUT);
  pinMode(EN3, OUTPUT); pinMode(IN5, OUTPUT);  pinMode(IN6, OUTPUT); pinMode(IN7, OUTPUT);  pinMode(IN8, OUTPUT); pinMode(EN4, OUTPUT);
}


void jalan(int gerak[], int pwm) {
  int pwm_baru = pwm - 100;
  int pwm_e1  = pwm+60;
  int pwm_e2  = pwm+10;
  int pwm_e3  = pwm+10;
  int pwm_e4  = pwm-60;
  if (gerak == curve_kanan) {
    analogWrite(EN1, pwm_e1);  analogWrite(EN2, (pwm));  analogWrite(EN3, pwm);  analogWrite(EN4, pwm / 2);
  }
  else if (gerak == curve_kiri) {
    analogWrite(EN1, (pwm_e1 / 2));  analogWrite(EN2, (pwm));  analogWrite(EN3, pwm / 2);  analogWrite(EN4, pwm);
  }
  else {
    analogWrite(EN1, pwm_e1);  analogWrite(EN2, (pwm_e2));  analogWrite(EN3, pwm_e3);  analogWrite(EN4, pwm_e4);
  }
  for (int i = 0; i < 8; i++) {
    digitalWrite(pinMotor(i), gerak[i]);
  }
}
