#include "CFG.h"
#include "GYRO_v2.h"
#include "MOTOR.h"
#include "PID_v2.h"
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

    yaw = getYaw();
    output1 = calculatePID(yaw, setpoint1, Kp1, Ki1, Kd1, lastError1, integral1, output1);
    gerak(PUTAR,output1);
    tampil(yaw, output1, x, y, jarak, sisi, persentase);

    /*
  //------------------------------------------------------------------------baca yaw
  if (b == 1) {
    detect();
    for (int a =0; a < 220; a++) {
      if (a < 180) {
        //        analogWrite(EN1, a);

        jalan(maju, a);
        Serial.print("speed: "); Serial.println(a);
        //        digitalWrite(IN1, HIGH);
        //        digitalWrite(IN2, LOW);
        delay(20);
        //        lcd.setCursor(10, 0);
        //        lcd.print("e="); lcd.print(a);
      }
      else if (a > 180) {
        while (1) {
          jalan(stopp, a);
          //          analogWrite(EN1, a);

          //        jalan(rot_kanan, a);
          Serial.print("speed: "); Serial.println(a);
          //          digitalWrite(IN1, 0);
          //          digitalWrite(IN2, 0);
          delay(20);
        }

      }
    }
  }
  */
}


void maju_grak() {
  if (int(yaw) < -1) {
    jalan(curve_kiri, 180);
  }
  else if (int(yaw) > 1) {
    jalan(curve_kanan, 180);
  }
  else {
    jalan(maju, 180);
  }
}
