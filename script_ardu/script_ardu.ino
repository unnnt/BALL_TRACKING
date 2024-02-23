#include "CFG.h"
#include "GYRO.h"
#include "MOTOR.h"
#include "PID.h"

void setup() {
  DEBUG_BEGIN(115200);
  setup_pinmotor();
  setup_mpu();
  SERVO_PIN(9);
}

void loop() {
//  if (Serial.available() > 0) {
    int nilai_analog = random(0,100);  // Baca nilai analog dari serial
    nilai_analog = constrain(nilai_analog, 0, 640);
    DEBUG_PRINTLN(nilai_analog);
    int pos_servo = map(nilai_analog, 0, 640, 0, 180);
    SERVO_WRITE(pos_servo);  // Kontrol servo berdasarkan nilai analog
//  }
}
