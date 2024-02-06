#include <Servo.h>

Servo myServo;

double setpoint = 320.0;  // Nilai tengah koordinat kamera
double input, output;
double Kp = 1.0;  // Konstanta Proporsional
double Ki = 0.1;  // Konstanta Integral
double Kd = 0.01; // Konstanta Derivatif

unsigned long lastTime = 0;
double elapsedTime, error, lastError;
double cumError, rateError;

void setup() {
  Serial.begin(115200);
  myServo.attach(9);  // Hubungkan servo ke pin 9
}

void loop() {
//  if (Serial.available() > 0) {
    int nilai_analog = Serial.parseInt();  // Baca nilai analog dari serial
    nilai_analog = constrain(nilai_analog, 0, 640);

    int pos_servo = map(nilai_analog, 0, 640, 0, 180);
    myServo.write(pos_servo);  // Kontrol servo berdasarkan nilai analog
//  }
}
