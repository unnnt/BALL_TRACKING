#include <Servo.h>

Servo myServo;

void setup() {
  Serial.begin(9600);
  myServo.attach(9);  // Hubungkan servo ke pin 9
}

void loop() {
  if (Serial.available() > 0) {
    int nilai_analog = Serial.parseInt();  // Baca nilai analog dari serial
    nilai_analog = constrain(nilai_analog, 0, 640);

    int pos_servo = map(nilai_analog, 0, 640, 0, 180);
    myServo.write(pos_servo);  // Kontrol servo berdasarkan nilai analog
  }
}
