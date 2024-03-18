#include "CFG.h"
#include "PID_v2.h"
#include "GYRO.h"
#include "MOTOR.h"
#include "DETECT.h"

int b;

void setup() {
  DEBUG_BEGIN(115200);
  setup_pinmotor();
  setup_mpu();
  SERVO_PIN(9);
  if (!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3C for 128x32
    Serial.println(F("SSD1306 allocation failed"));
    for (;;); // Don't proceed, loop forever
  }
  b = 1;
}

void loop() {
  if (b == 1) {
    for (int a = 0; a <= 5; a++) {

      if (a == 5) {
        a = 41;
        b = 1;
        jalan(stopp, 120);
      }
      else {
        Serial.print(getYaw()); Serial.print("\t");
        output1 = calculatePID(getYaw(), setpoint1, Kp1, Ki1, Kd1, lastError1, integral1, output1);
        Serial.println(output1);
        maju_grak();
        detect();        
        tampil(1, output1, x, y);
      }
    }
  }
  else {
    jalan(stopp, 120);
  }
}

void tampil(int text_size, double PID, int X, int Y) {
  display.clearDisplay();
  display.setTextSize(text_size);
  display.setTextColor(WHITE);
  display.setCursor(1, 5);
  display.print("YAW = "); display.println(getYaw());
  display.print("X,Y = "); display.print(X); display.print(","); display.println(Y);
  display.print("Error = "); display.println(PID);

  display.display();
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
