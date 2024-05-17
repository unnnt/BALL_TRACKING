#include "CFG.h"
#include "PID_v2.h"
#include "GYRO.h"
#include "MOTOR.h"
#include "DETECT.h"

int b;

void setup() {
  lcd.init();
  lcd.backlight();
  DEBUG_BEGIN(115200);
  setup_pinmotor();
  setup_mpu();
  SERVO_PIN(9);
  b = 1;
}

void loop() {
  Serial.print("getYaw = ");Serial.print(getYaw()); Serial.println("\t");
  if (b == 1) {
    for (int a = 0; a <= 5; a++) {

      if (a == 5) {
        a = 41;
        b = 1;
        jalan(stopp, 120);
      }
      else {
        new_yaw = 2 * getYaw();
        Serial.print("new = ");Serial.print(new_yaw); Serial.print("\t");
        output1 = calculatePID(new_yaw, setpoint1, Kp1, Ki1, Kd1, lastError1, integral1, output1);
        Serial.println(output1);
        maju_grak();
        detect();        
        tampil(new_yaw, output1, x, y);
      }
    }
  }
  else {
    jalan(stopp, 120);
  }
}

void tampil(float new_yaw, double PID, int X, int Y) {
  lcd.setCursor(0, 0); lcd.print("Y=");
  lcd.setCursor(2, 0); lcd.print(new_yaw);
  lcd.setCursor(0, 1); lcd.print(X); lcd.print(","); lcd.println(Y);
  lcd.setCursor(10, 0); lcd.print("e="); lcd.print(PID);
}

void putar() {
  if (int(output1) < -1) {
    jalan(kiri, 90);
  }
  else if (int(output1) > 1) {
    jalan(kanan, 90);
  }
  else {
    jalan(stopp, 70);
  }
}

void maju_grak() {
  if (int(output1) < -1) {
    jalan(curve_kiri, 180);
  }
  else if (int(output1) > 1) {
    jalan(curve_kanan, 180);
  }
  else {
    jalan(maju, 180);
  }
}
