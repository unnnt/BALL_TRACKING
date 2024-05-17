#include <Wire.h>
#include <MPU6050.h>
#include <SPI.h>

MPU6050 mpu;

unsigned long timer = 0;
float timeStep = 0.01;

float yaw = 0;

void setup_mpu() {
  while (!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G)) {
    DEBUG_PRINTLN("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }
  mpu.calibrateGyro();
  mpu.setThreshold(0);
}

float getYaw() {
//  /*
    timer = millis();
    Vector norm = mpu.readNormalizeGyro();
    yaw = fmod(yaw + norm.ZAxis * timeStep ,360);

    //  if (yaw < 0) {
    //    yaw = 360 + yaw;
    //  }

    delay((timeStep * 1000) - (millis() - timer));
//  */
  return yaw;
}
