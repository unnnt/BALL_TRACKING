#include "SG_PID.h"
#include <Servo.h>

Servo myServo;
#include <SoftwareSerial.h>

SoftwareSerial mySerial(11, 10); // RX, TX

PID PID;
void setup() {
  mySerial.begin(9600);
  Serial.begin(115200);
  PID.param(1, 0.1, 0.02, INTEGRAL);
  PID.constraint(-255, 255);
  PID.setPoint(50);
  PID.readSensor(0);
  PID.timeSampling(1);
  PID.showParam();
  myServo.attach(9);
  Serial.println();
}

void loop() {
  //  int valSensor = random(-20, 20);
  for (int a = 0; a < 100 ; a+=10) {
//    int nilai_analog = Serial.parseInt();// Baca nilai analog dari serial
    //    nilai_analog = constrain(nilai_analog, 0, 640);
    //  mySerial.print("AR 1 :");

    //    nilai_analog = map(nilai_analog, 0, 640, 0, 180);

    PID.readSensor(a);

    Serial.print(a); Serial.print("\t");

    PID.calc();

//    delay(1000);
      PID.showUnitPID();
    //  myServo.write(PID.showPID());
    Serial.print(PID.showPID());
//    mySerial.println(PID.showPID(), 4);
    Serial.println();
  }
}
