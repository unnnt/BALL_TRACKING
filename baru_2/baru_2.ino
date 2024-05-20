#include "CFG.h"
#include "PID_v2.h"
#include "GYRO_v2.h"
#include "MOTOR.h"
#include "DETECT.h"
#include "LCD.h"

int b;

void setup() {
  lcd.init();
  lcd.backlight();
  DEBUG_BEGIN(115200);
  setup_mpu();
  setup_pinmotor();
  setup_mpu();
  SERVO_PIN(9);
  b = 1;
}

void loop() {
  //------------------------------------------------------------------------baca yaw
  float yaw = getYaw(thd);
  Serial.print("yaw: "); Serial.println(yaw);
  detect();
  tampil(yaw, output1, x, y, jarak, sisi, persentase);


  //
  //    delay(100); // Delay to make the output readable
  /*
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
  */
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
