// Motor depan
#define EN1 3
#define IN1 7
#define IN2 2
#define IN3 4
#define IN4 5
#define EN2 6

// Motor belakang
#define EN3 11
#define IN5 13
#define IN6 12
#define IN7 9
#define IN8 8
#define EN4 10

int maju[]       = {HIGH  , LOW  , HIGH , LOW  , HIGH , LOW  , HIGH , LOW};
int mudur[]      = {LOW   , HIGH , LOW  , HIGH , LOW  , HIGH , LOW  , HIGH};
int kiri[]       = {HIGH  , LOW  , HIGH , LOW  , LOW  , LOW  , HIGH , LOW};
int kanan[]      = {LOW   , HIGH , LOW  , HIGH , HIGH , LOW  , LOW  , LOW};
int rot_kiri[]   = {HIGH  , LOW  , HIGH , LOW  , LOW  , HIGH , LOW  , HIGH};
int rot_kanan[]  = {LOW   , HIGH , LOW  , HIGH , HIGH , LOW  , HIGH , LOW};
int stopp[]      = {LOW   , LOW  , LOW  , LOW  , LOW  , LOW  , LOW  , LOW};

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
  analogWrite(EN1, pwm);
  analogWrite(EN2, pwm);
  analogWrite(EN3, pwm);
  analogWrite(EN4, pwm);
  for (int i = 0; i < 8; i++) {
    digitalWrite(pinMotor(i), gerak[i]);
  }
}
